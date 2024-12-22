variable "token" {
  description = "Yandex Cloud API token"
  type        = string
  sensitive   = true
}

variable "cloud_id" {
  description = "Yandex Cloud ID"
  type        = string
}

variable "folder_id" {
  description = "Yandex Cloud Folder ID"
  type        = string
}

variable "zone" {
  description = "Yandex Cloud Zone"
  type        = string
  default     = "ru-central1-a"
}

variable "service_account_id" {
  description = "Service Account ID"
  type        = string
}

variable "github_access_token" {
  description = "GitHub Access Token"
  type        = string
  sensitive   = true
}

variable "postgres_host" {
  description = "PostgreSQL Host"
  type        = string
}

variable "postgres_port" {
  description = "PostgreSQL Port"
  type        = number
  default     = 5432
}

variable "postgres_user" {
  description = "PostgreSQL User"
  type        = string
}

variable "postgres_password" {
  description = "PostgreSQL Password"
  type        = string
  sensitive   = true
}

variable "postgres_db" {
  description = "PostgreSQL Database"
  type        = string
}