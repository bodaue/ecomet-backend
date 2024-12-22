data "archive_file" "function_zip" {
  type        = "zip"
  output_path = "${path.module}/function.zip"
  source_dir  = "${path.module}/../cloud_function"
  excludes    = ["__pycache__", "*.pyc", "*.pyo"]
}

resource "yandex_iam_service_account" "function_sa" {
  name        = "github-stats-function-sa"
  description = "Service account for GitHub Stats Cloud Function"
}

resource "yandex_resourcemanager_folder_iam_member" "function_invoker" {
  folder_id = var.folder_id
  role      = "functions.functionInvoker"
  member    = "serviceAccount:${yandex_iam_service_account.function_sa.id}"
}

resource "yandex_function" "github_stats" {
  name               = "github-stats-updater"
  description        = "Function to update GitHub repository statistics"
  user_hash          = data.archive_file.function_zip.output_base64sha256
  runtime            = "python312"
  entrypoint         = "cloud_function.github.parser.handler"
  memory             = "256"
  execution_timeout  = "300"
  service_account_id = var.service_account_id

  environment = {
    GITHUB_ACCESS_TOKEN = var.github_access_token
    POSTGRES_HOST       = var.postgres_host
    POSTGRES_PORT       = var.postgres_port
    POSTGRES_USER       = var.postgres_user
    POSTGRES_PASSWORD   = var.postgres_password
    POSTGRES_DB         = var.postgres_db
  }

  content {
    zip_filename = data.archive_file.function_zip.output_path
  }
}

resource "yandex_function_trigger" "timer" {
  name        = "github-stats-timer"
  description = "Timer trigger for GitHub Stats updater"
  timer {
    cron_expression = "0 */6 * * * *" # Every 6 hours
  }

  function {
    id                 = yandex_function.github_stats.id
    service_account_id = var.service_account_id
  }
}