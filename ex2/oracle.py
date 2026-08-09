#!/usr/bin/env python3
"""oracle.py - read configuration from environment variables.

Loads development settings from a .env file using python-dotenv.
Real environment variables take precedence over .env values.
The program validates the configuration and reports missing values.
"""

import os
import sys


PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_FILE = os.path.join(PROJECT_DIR, ".env")

REQUIRED_VARS: list[str] = [
    "MATRIX_MODE",
    "DATABASE_URL",
    "API_KEY",
    "LOG_LEVEL",
    "ZION_ENDPOINT",
]

DEFAULTS: dict[str, str] = {
    "MATRIX_MODE": "development",
    "DATABASE_URL": "postgresql://localhost:5432/matrix",
    "API_KEY": "",
    "LOG_LEVEL": "DEBUG",
    "ZION_ENDPOINT": "https://zion.local/api",
}


def load_environment_file() -> bool:
    """Load the .env file when python-dotenv is available."""
    if not os.path.exists(ENV_FILE):
        print(
            "WARNING: .env file not found; "
            "using environment variables and defaults."
        )
        return False

    try:
        from dotenv import load_dotenv  # type: ignore[import-not-found]
    except ImportError:
        print(
            "WARNING: python-dotenv is not installed; "
            "skipping .env loading."
        )
        print(
            "Install it with: "
            "python3 -m pip install python-dotenv"
        )
        return False

    try:
        loaded = load_dotenv(ENV_FILE)
    except (OSError, UnicodeError) as error:
        print(
            "WARNING: could not read .env file: {}".format(error)
        )
        return False

    if not loaded:
        print("WARNING: .env file could not be loaded.")
        return False

    return True


def load_configuration() -> dict[str, str]:
    """Load .env values and return the Matrix configuration."""
    load_environment_file()

    configuration: dict[str, str] = {}

    for variable in REQUIRED_VARS:
        configuration[variable] = os.environ.get(
            variable,
            DEFAULTS[variable],
        )

    return configuration


def find_missing_vars(config: dict[str, str]) -> list[str]:
    """Return missing or invalid configuration variables."""
    missing: list[str] = []

    for variable in REQUIRED_VARS:
        if not config[variable]:
            missing.append(variable)

    if config["MATRIX_MODE"] not in {
        "development",
        "production",
    }:
        if "MATRIX_MODE" not in missing:
            missing.append("MATRIX_MODE")

    return missing


def is_development(config: dict[str, str]) -> bool:
    """Return whether the Matrix runs in development mode."""
    return config["MATRIX_MODE"] == "development"


def label_database(config: dict[str, str]) -> str:
    """Describe where the database connection points."""
    database_url = config["DATABASE_URL"]

    if not database_url:
        return "Connection URL missing"

    if (
        "localhost" in database_url
        or "127.0.0.1" in database_url
    ):
        return "Connected to local instance"

    if "prod" in database_url:
        return "Connected to production instance"

    return "Connected to remote instance"


def label_api_key(config: dict[str, str]) -> str:
    """Describe the API authentication state."""
    if not config["API_KEY"]:
        return "No API key configured"

    if is_development(config):
        return "Authenticated (development key)"

    return "Authenticated (production key)"


def label_zion(config: dict[str, str]) -> str:
    """Describe the resistance network status."""
    if not config["ZION_ENDPOINT"]:
        return "Offline - endpoint missing"

    return "Online"


def print_security_checks(config: dict[str, str]) -> None:
    """Run security checks and print their results."""
    print("Environment security check:")

    print("  [OK] API key is not displayed")

    gitignore = os.path.join(PROJECT_DIR, ".gitignore")

    try:
        with open(
            gitignore,
            "r",
            encoding="utf-8",
        ) as gitignore_file:
            ignored_lines = gitignore_file.read().splitlines()

        env_ignored = any(
            line.strip() == ".env"
            for line in ignored_lines
        )

    except (OSError, UnicodeError):
        env_ignored = False

    ignore_status = "OK" if env_ignored else "WARN"
    print(
        "  [{}] .env file properly ignored in git".format(
            ignore_status
        )
    )

    if os.path.exists(ENV_FILE):
        print("  [OK] .env file found")
    else:
        print("  [WARN] No .env file found, using defaults")


def print_missing_warnings(missing: list[str]) -> None:
    """Print a warning for each missing configuration variable."""
    print("Missing or invalid configuration:")

    for variable in missing:
        print("  - {} is missing or invalid".format(variable))


def show_configuration(
    config: dict[str, str],
    missing: list[str],
) -> None:
    """Print the loaded configuration and security checks."""
    print("ORACLE STATUS: Reading the Matrix...")
    print()
    print("Configuration loaded:")

    mode = config["MATRIX_MODE"]

    if mode not in {"development", "production"}:
        mode = "invalid"

    print("  Mode: {}".format(mode))
    print("  Database: {}".format(label_database(config)))
    print("  API Access: {}".format(label_api_key(config)))
    print("  Log Level: {}".format(config["LOG_LEVEL"]))
    print("  Zion Network: {}".format(label_zion(config)))

    if mode == "production":
        print()
        print(
            "PRODUCTION MODE: handling production traffic carefully."
        )

    if missing:
        print()
        print_missing_warnings(missing)

    print()
    print_security_checks(config)


def main() -> None:
    """Load and display the Matrix configuration."""
    config = load_configuration()
    missing = find_missing_vars(config)
    show_configuration(config, missing)

    if missing:
        sys.exit(1)


if __name__ == "__main__":
    main()
