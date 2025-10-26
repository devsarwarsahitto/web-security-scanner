import os

VERSION = "1.0.0"
AUTHOR = "Sarwar Jahan Sahitto"
GITHUB = "https://github.com/devsarwarsahitto"

DEFAULT_TIMEOUT = 10
DEFAULT_THREADS = 10
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
DEFAULT_RETRIES = 2
DEFAULT_RATE_LIMIT = 0.1

OUTPUT_DIR = "scans"
ENV_FILES_DIR = os.path.join(OUTPUT_DIR, "env_files")
REPORTS_DIR = os.path.join(OUTPUT_DIR, "reports")

ENV_PATHS = [
    ".env",
    "env",
    ".env.local",
    ".env.production",
    ".env.development",
    ".env.staging",
    ".env.test",
    ".env.example",
    ".env.backup",
    ".env.old",
    "config/.env",
    "app/.env",
    "src/.env",
    "backend/.env",
    "api/.env",
]

BACKUP_FILES = [
    "backup.sql",
    "backup.zip",
    "backup.tar.gz",
    "database.sql",
    "db.sql",
    "dump.sql",
    "site.zip",
    "www.zip",
    "backup.tar",
    "backup.bak",
    "config.bak",
    "web.config.bak",
    ".htaccess.bak",
]

ADMIN_PANELS = [
    "admin",
    "admin/",
    "administrator",
    "admin/login",
    "admin/index.php",
    "admin.php",
    "login.php",
    "wp-admin",
    "wp-login.php",
    "phpmyadmin",
    "cpanel",
    "webmail",
    "administrator/",
    "moderator/",
    "controlpanel/",
    "adminpanel/",
    "admin1/",
    "admin2/",
    "admin/account.php",
    "admin/index.html",
    "admin/admin.php",
    "admin_area/",
]

GIT_PATHS = [
    ".git/",
    ".git/config",
    ".git/HEAD",
    ".git/logs/HEAD",
    ".gitignore",
]

COMMON_PORTS = [80, 443, 8080, 8443, 8000, 3000, 5000]
