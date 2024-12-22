import asyncio
import logging
from datetime import timedelta, datetime, UTC

from parsers.github.client import GitHubClient
from src.core.settings import create_settings

# Настраиваем логирование
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def main() -> None:
    # Создаем тестовые настройки
    settings = create_settings()

    try:
        async with GitHubClient(settings) as client:
            # Получаем топ репозитории
            logger.info("Fetching top repositories...")
            async for repo in client.get_top_repositories(limit=5):
                print(repo)
            # Получаем активность конкретного репозитория
            repo_owner = "microsoft"
            repo_name = "vscode"
            end_date = datetime.now(UTC).today()
            start_date = end_date - timedelta(days=7)

            commit_count = 0
            authors = set()

            async for commit in client.get_repository_activity(
                owner=repo_owner, repo=repo_name, since=start_date, until=end_date
            ):
                print(commit)
                commit_count += 1
                authors.add(commit.author)

    except Exception as e:
        logger.exception(f"Error occurred: {e!s}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
