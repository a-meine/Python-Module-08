#!/usr/bin/env python3
"""oracle.py - read configuration from environment variables.

Loads development settings from a .env file with python-dotenv.
Real environment variables take priority over .env values.
Displays the configuration safely and reports missing values.
"""

import os
import sys


PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_FILE = os.path.join(PROJECT_DIR, ".env")
GITIGNORE_FILE = os.path.join(PROJECT_DIR, ".gitignore")

REQUIRED_VARS: list[str] = [
    "MATRIX_MODE",
    "DATABASE_URL",
    "API_KEY",
    "LOG_LEVEL",
    "ZION_ENDPOINT",
]


def load_environment_file() -> bool:
    """Load .env when it and python-dotenv are available."""
    if not os.path.exists(ENV_FILE):
        print("WARNING: .env file not found.")
        print("Using environment variables only.")
        return False

    try:
        from dotenv import load_dotenv  # type: ignore[import-not-found]
    except ImportError:
        print("WARNING: python-dotenv is not installed.")
        print("Install it with: python3 -m pip install python-dotenv")
        print("Using environment variables only.")
        return False

    try:
        loaded = load_dotenv(ENV_FILE, override=False)
    except (OSError, UnicodeError) as error:
        print("WARNING: could not read .env: {}".format(error))
        return False

    if not loaded:
        print("WARNING: .env file was found but no values were loaded.")
        return False

    return True


def load_configuration() -> dict[str, str]:
    """Load .env and return the required environment configuration."""
    load_environment_file()

    configuration: dict[str, str] = {}

    for variable in REQUIRED_VARS:
        configuration[variable] = os.environ.get(variable, "").strip()

    return configuration


def find_configuration_errors(
    config: dict[str, str],
) -> list[str]:
    """Return missing or invalid configuration messages."""
    errors: list[str] = []

    for variable in REQUIRED_VARS:
        if not config[variable]:
            errors.append("{} is missing".format(variable))

    mode = config["MATRIX_MODE"]

    if mode and mode not in {"development", "production"}:
        errors.append(
            "MATRIX_MODE must be 'development' or 'production'"
        )

    return errors


def label_database(config: dict[str, str]) -> str:
    """Return a safe database configuration status."""
    database_url = config["DATABASE_URL"]

    if not database_url:
        return "Not configured"

    if (
        "localhost" in database_url
        or "127.0.0.1" in database_url
    ):
        return "Connected to local instance"

    return "Configured for remote instance"


def label_api_access(config: dict[str, str]) -> str:
    """Return a safe API configuration status without exposing the key."""
    if not config["API_KEY"]:
        return "Not configured"

    return "Authenticated"


def label_zion_network(config: dict[str, str]) -> str:
    """Return a safe Zion endpoint configuration status."""
    if not config["ZION_ENDPOINT"]:
        return "Offline - endpoint missing"

    return "Online"


def environment_ignores_dotenv() -> bool:
    """Return whether .gitignore contains an exact .env entry."""
    try:
        with open(
            GITIGNORE_FILE,
            "r",
            encoding="utf-8",
        ) as gitignore_file:
            lines = gitignore_file.read().splitlines()
    except (OSError, UnicodeError):
        return False

    return any(line.strip() == ".env" for line in lines)


def print_security_checks() -> None:
    """Print configuration security checks."""
    print("Environment security check:")
    print("  [OK] API_KEY is never displayed")

    if environment_ignores_dotenv():
        print("  [OK] .env file is ignored by Git")
    else:
        print("  [WARN] Add '.env' to .gitignore")

    print("  [OK] Environment variables can override .env values")


def print_errors(errors: list[str]) -> None:
    """Print configuration warnings."""
    print("Missing or invalid configuration:")

    for error in errors:
        print("  - {}".format(error))


def show_configuration(
    config: dict[str, str],
    errors: list[str],
) -> None:
    """Display the configuration without exposing secrets."""
    mode = config["MATRIX_MODE"]

    print("ORACLE STATUS: Reading the Matrix...")
    print()
    print("Configuration loaded:")
    print("  Mode: {}".format(mode or "Not configured"))
    print("  Database: {}".format(label_database(config)))
    print("  API Access: {}".format(label_api_access(config)))
    print("  Log Level: {}".format(
        config["LOG_LEVEL"] or "Not configured"
    ))
    print("  Zion Network: {}".format(label_zion_network(config)))

    if mode == "development":
        print()
        print(
            "DEVELOPMENT MODE: local configuration is active."
        )

    elif mode == "production":
        print()
        print(
            "PRODUCTION MODE: production configuration is active."
        )

    if errors:
        print()
        print_errors(errors)

    print()
    print_security_checks()


def main() -> None:
    """Load and display Matrix configuration."""
    config = load_configuration()
    errors = find_configuration_errors(config)

    show_configuration(config, errors)

    if errors:
        sys.exit(1)

    print("\n\nThe Oracle sees all configurations.")


if __name__ == "__main__":
    main()
