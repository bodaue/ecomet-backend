import asyncio
import logging
from collections import defaultdict
from collections.abc import AsyncGenerator
from datetime import datetime, date, timedelta, UTC

import asyncpg
from asyncpg import Pool

from cloud_function.github.client import GitHubClient
from cloud_function.github.schemas import GitHubRepo, GitHubCommit
from cloud_function.github.settings import ParserSettings, create_parser_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class GitHubParser:
    def __init__(self, pool: Pool, settings: ParserSettings) -> None:
        self._pool = pool
        self._settings = settings
        self._github_client = GitHubClient(settings)

    async def _update_top_repos(self, repos: list[GitHubRepo]) -> None:
        """
        Update top repositories data in the database.

        Args:
            repos: List of repositories fetched from GitHub
        """
        async with self._pool.acquire() as conn, conn.transaction():
            try:
                # Get current positions for calculating position changes
                current_positions = await conn.fetch(
                    """
                    SELECT owner, repo, position_cur
                    FROM top100
                    """
                )
                position_map = {
                    (row["owner"], row["repo"]): row["position_cur"]
                    for row in current_positions
                }

                # Clear current data
                await conn.execute("TRUNCATE TABLE top100, activity CASCADE")

                # Insert new data with position tracking
                for position, repo in enumerate(repos, 1):
                    # Get previous position or use current if not found
                    prev_position = position_map.get(
                        (repo.owner_login, repo.name), position
                    )

                    await conn.execute(
                        """
                        INSERT INTO top100 (
                            repo, owner, position_cur, position_prev,
                            stars, watchers, forks, open_issues, language
                        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                        """,
                        repo.name,
                        repo.owner_login,
                        position,
                        prev_position,
                        repo.stars,
                        repo.watchers,
                        repo.forks,
                        repo.open_issues,
                        repo.language,
                    )

            except Exception as e:
                logger.exception(f"Error updating top repositories: {e}")
                raise

    async def _process_repo_activity(
        self,
        owner: str,
        repo: str,
        since: date,
        until: date,
        commits: AsyncGenerator[GitHubCommit, None],
    ) -> None:
        commit_data = defaultdict(lambda: {"commits": 0, "authors": set()})

        try:
            # Process all commits
            async for commit in commits:
                commit_date = commit.date.date()
                if since <= commit_date <= until:
                    commit_data[commit_date]["commits"] += 1
                    commit_data[commit_date]["authors"].add(commit.author)

            async with self._pool.acquire() as conn:
                # Get repository ID
                repo_id = await conn.fetchval(
                    "SELECT id FROM top100 WHERE owner = $1 AND repo = $2", owner, repo
                )

                if not repo_id:
                    logger.warning(f"Repository {owner}/{repo} not found in top100")
                    return

                # Update activity data in transaction
                async with conn.transaction():
                    # Remove old data for this period
                    await conn.execute(
                        """
                        DELETE FROM activity
                        WHERE repository_id = $1 AND date BETWEEN $2 AND $3
                        """,
                        repo_id,
                        since,
                        until,
                    )

                    # Insert new activity data
                    for commit_date, data in commit_data.items():
                        await conn.execute(
                            """
                            INSERT INTO activity (
                                repository_id, date, commits, authors
                            ) VALUES ($1, $2, $3, $4)
                            """,
                            repo_id,
                            commit_date,
                            data["commits"],
                            list(data["authors"]),
                        )

        except Exception as e:
            logger.exception(f"Error processing activity for {owner}/{repo}: {e}")
            raise

    async def update_data(self) -> None:
        """Main method to update all GitHub data."""
        try:
            async with self._github_client as client:
                # Fetch and update top repositories
                logger.info("Fetching top repositories...")
                repos = [repo async for repo in client.get_top_repositories(limit=100)]
                await self._update_top_repos(repos)
                logger.info("Top repositories updated successfully")

                # Update activity for each repository
                logger.info("Updating repository activity...")
                end_date = datetime.now(UTC).date()
                start_date = end_date - timedelta(days=30)

                for repo in repos:
                    try:
                        logger.info(f"Processing {repo.owner_login}/{repo.name}")
                        await self._process_repo_activity(
                            owner=repo.owner_login,
                            repo=repo.name,
                            since=start_date,
                            until=end_date,
                            commits=client.get_repository_activity(
                                owner=repo.owner_login,
                                repo=repo.name,
                                since=start_date,
                                until=end_date,
                            ),
                        )
                    except Exception as e:
                        logger.exception(
                            f"Error processing {repo.owner_login}/{repo.name}: {e}"
                        )
                        # Continue with next repo if one fails
                        continue

                logger.info("Repository activity update completed")

        except Exception as e:
            logger.exception(f"Error updating GitHub data: {e}")
            raise


async def main() -> None:
    """Main function for running the parser directly."""
    settings = create_parser_settings()

    # Create database pool
    pool = await asyncpg.create_pool(
        settings.postgres.build_dsn(), min_size=2, max_size=10
    )

    if not pool:
        msg = "Failed to create database pool"
        raise RuntimeError(msg)

    try:
        parser = GitHubParser(pool, settings)
        await parser.update_data()
    finally:
        await pool.close()


def handler(event: dict, context: dict) -> dict:  # noqa: ARG001
    """
    Cloud Function handler.

    Args:
        event: Cloud function event data
        context: Cloud function context

    Returns:
        dict: Response with status code and message
    """
    try:
        asyncio.run(main())
    except Exception as e:
        logger.exception(f"Error in cloud function: {e}")
        return {"statusCode": 500, "body": f"Error updating data: {e!s}"}
    else:
        return {"statusCode": 200, "body": "Data updated successfully"}


if __name__ == "__main__":
    asyncio.run(main())
