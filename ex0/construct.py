#!/usr/bin/env python3
"""construct.py - the construct sentinel.

Detects whether Python runs inside a virtual environment, reports
information about the current Python environment, shows the
difference between global and virtual package locations and, when
running globally, explains how to enter the construct.
"""

import os
import site
import sys


def inside_virtualenv() -> bool:
    """Return True when a virtual environment is active."""
    return bool(os.environ.get("VIRTUAL_ENV")) or sys.prefix != sys.base_prefix


def virtualenv_name() -> str:
    """Return the name of the active virtual environment."""
    virtual_env = os.environ.get("VIRTUAL_ENV")
    if virtual_env:
        return os.path.basename(virtual_env)
    return os.path.basename(sys.prefix)


def virtualenv_root() -> str:
    """Return the root directory of the active virtual environment."""
    return os.environ.get("VIRTUAL_ENV") or sys.prefix


def site_packages_for(prefix: str) -> str:
    """Build the site-packages path for a given interpreter prefix."""
    version = "python{0}.{1}".format(sys.version_info.major,
                                     sys.version_info.minor)
    return os.path.join(prefix, "lib", version, "site-packages")


def current_site_packages() -> str:
    """Return the site-packages path of the current interpreter."""
    return site.getsitepackages()[0]


def global_site_packages() -> str:
    """Return the site-packages path of the global interpreter."""
    return site_packages_for(sys.base_prefix)


def print_global_report() -> None:
    """Print the report produced outside a virtual environment."""
    print("MATRIX STATUS: You're still plugged in")
    print()
    print("Current Python: {}".format(sys.executable))
    print("Virtual Environment: None detected")
    print()
    print("WARNING: You're in the global environment!")
    print("The machines can see everything you install.")
    print()
    print("To enter the construct, run:")
    print("python -m venv matrix_env")
    print("source matrix_env/bin/activate  # On Unix")
    print("matrix_env\\Scripts\\activate  # On Windows")
    print()
    print("Then run this program again.")
    print()
    print("Package locations (global vs virtual):")
    print("  Global : {}".format(global_site_packages()))
    print("  Current: {}".format(current_site_packages()))


def print_virtualenv_report() -> None:
    """Print the report produced inside a virtual environment."""
    print("MATRIX STATUS: Welcome to the construct")
    print()
    print("Current Python: {}".format(sys.executable))
    print("Virtual Environment: {}".format(virtualenv_name()))
    print("Environment Path: {}".format(virtualenv_root()))
    print()
    print("SUCCESS: You're in an isolated environment!")
    print("Safe to install packages without affecting")
    print("the global system.")
    print()
    print("Package installation path:")
    print("  {}".format(current_site_packages()))
    print()
    print("Package locations (global vs virtual):")
    print("  Global : {}".format(global_site_packages()))
    print("  Current: {}".format(current_site_packages()))


def main() -> None:
    """Dispatch to the report matching the current environment."""
    if inside_virtualenv():
        print_virtualenv_report()
    else:
        print_global_report()


if __name__ == "__main__":
    main()
