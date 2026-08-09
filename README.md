# Python Module 08 — The Matrix

A 42 project covering Python virtual environments, package management with `pip` and Poetry, and environment configuration with `.env` files.

> “Welcome to the real world.” — Morpheus

## Project structure

```text
.
├── ex0/
│   └── construct.py       # virtual-environment detection
├── ex1/
│   ├── loading.py         # NumPy / pandas / Matplotlib analysis
│   ├── requirements.txt   # pip dependencies
│   └── pyproject.toml     # Poetry dependencies
├── ex2/
│   ├── oracle.py          # environment configuration
│   ├── .env.example       # safe configuration template
│   └── .gitignore         # prevents committing .env
└── README.md
```

General rules: Python 3.10+, flake8, type annotations checked with `mypy`, and safe error handling.

---

## pip vs Poetry

| Topic | `pip` + `venv` | Poetry |
|---|---|---|
| Main role | Installs packages | Manages dependencies and project workflow |
| Environment | Create and activate manually | Selects or creates a project environment |
| Dependency file | `requirements.txt` | `pyproject.toml` |
| Exact resolved versions | Pin manually | `poetry.lock` |
| Run a command | Activate the venv, then run | `poetry run COMMAND` |
| Packaging | Usually other tools | Includes build/publish commands |

```text
pip:    You manage the environment; pip installs packages in it.
Poetry: Poetry manages dependencies, locking, environments, and project workflow.
```

### Minimal pip workflow

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
deactivate
```

Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

### Minimal Poetry workflow

```bash
poetry init
poetry add "requests==2.32.3"
poetry install
poetry run python app.py
```

Useful commands:

```bash
poetry env info
poetry show --tree
poetry update requests
poetry show --outdated
```

`pyproject.toml` declares allowed dependency versions; `poetry.lock` records the exact resolved versions.

### Add requirements to Poetry

To add non-empty, uncommented entries from `requirements.txt`:

```bash
sed -e 's/#.*//' -e '/^[[:space:]]*$/d' requirements.txt | xargs poetry add
```

Review the result if the file contains URLs, extras, editable installs, or pip-specific options.

### Honorable mention: uv

`uv` supports both pip-style installation and project workflows:

```bash
uv init uv-demo
cd uv-demo
uv add requests
uv run python app.py
```

Or:

```bash
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

---

## Exercise 0 — Entering the Matrix

`ex0/construct.py` detects whether the interpreter runs inside a virtual environment and prints useful environment details.

```python
inside_venv = (
    bool(os.environ.get("VIRTUAL_ENV"))
    or sys.prefix != sys.base_prefix
)
```

| Check | Meaning |
|---|---|
| `VIRTUAL_ENV` | Usually set by activation scripts |
| `sys.prefix != sys.base_prefix` | Python is executing in a virtual environment |

The `sys.prefix` check also works when the venv interpreter is started directly without activating it first.

### Run it

```bash
# Outside a virtual environment
python3 ex0/construct.py

# Create and use a virtual environment
python3 -m venv matrix_env
source matrix_env/bin/activate
python3 ex0/construct.py
deactivate
```

The program reports the current interpreter, virtual-environment status, relevant package locations, and activation instructions when outside a venv.

---

## Exercise 1 — Loading Programs

`ex1/loading.py` demonstrates package management while running a small data-analysis pipeline.

| Package | Role |
|---|---|
| NumPy | Generates 1000 simulated Matrix data points |
| pandas | Loads CSV data and produces statistics |
| Matplotlib | Generates `matrix_analysis.png` |

The program detects missing packages, prints pip and Poetry installation guidance, generates the data with NumPy, writes it to CSV, analyzes it with pandas, and saves a chart with Matplotlib.

### Run with pip

```bash
cd ex1
python3 -m pip install -r requirements.txt
python3 loading.py
```

### Run with Poetry

```bash
cd ex1
poetry install
poetry run python loading.py
```

### Expected behavior

```text
LOADING STATUS: Loading programs...
Checking dependencies:
  [OK] numpy (...) - Numerical computation ready
  [OK] pandas (...) - Data manipulation ready
  [OK] matplotlib (...) - Visualization ready

Dependency management comparison:
pip:
  Configuration file: requirements.txt
  Install command: pip install -r requirements.txt

Poetry:
  Configuration file: pyproject.toml
  Install command: poetry install

Analyzing Matrix data...
Processing 1000 data points...
Generating visualization...
Analysis complete!
```

---

## Exercise 2 — Accessing the Mainframe

`ex2/oracle.py` demonstrates secure configuration through environment variables and `.env` files, loaded with `python-dotenv`.

### Required variables

| Variable | Purpose |
|---|---|
| `MATRIX_MODE` | `development` or `production` |
| `DATABASE_URL` | Data-storage connection string |
| `API_KEY` | Secret for an external service |
| `LOG_LEVEL` | Logging verbosity |
| `ZION_ENDPOINT` | Resistance-network URL |

### Configuration precedence

```text
1. Real environment variables
2. Values loaded from .env
3. Missing-configuration warnings
```

Local `.env` values are convenient for development. Existing shell environment variables take precedence, making production overrides possible.

### `.env.example`

This file is safe to commit because it contains only placeholder values:

```env
MATRIX_MODE=development
DATABASE_URL=postgresql://localhost:5432/matrix_dev
API_KEY=change-me-this-is-not-a-real-secret
LOG_LEVEL=DEBUG
ZION_ENDPOINT=https://zion.local/api
```

### `.gitignore`

```gitignore
.env
__pycache__/
*.pyc
```

`.env` must never be committed because it can contain real credentials, API keys, and private endpoints.

### Run it

```bash
# No configuration: warnings are shown safely
python3 ex2/oracle.py

# Create local configuration
cp ex2/.env.example ex2/.env
python3 ex2/oracle.py

# Shell variables override .env
MATRIX_MODE=production API_KEY=secret123 LOG_LEVEL=INFO python3 ex2/oracle.py
```

### Development and production

The same application code can use different configuration values:

```text
Development: local/test database, DEBUG logs, test endpoint.
Production:  remote/live database, INFO logs, live endpoint.
```

Example output messages:

```text
DEVELOPMENT MODE: Test configuration active.
Debug logging is enabled for local troubleshooting.
```

```text
PRODUCTION MODE: Live configuration active.
Use protected credentials and avoid debug logging.
```

---

## Virtual environments

A virtual environment isolates a project’s third-party packages while reusing the base Python interpreter and standard library.

```text
Base Python
├── Built-ins and standard library
├── Global site-packages
└── Virtual environment
    ├── Python executable
    ├── pip
    └── project-specific site-packages
```

| Component | Shared with base Python? | Isolated per venv? |
|---|---:|---:|
| Built-ins, such as `print()` | Yes | No |
| Standard library, such as `os` | Yes | No |
| Third-party packages | No, by default | Yes |
| Tools installed with pip | No, by default | Yes |

### Essential commands

```bash
# Create a venv
python3 -m venv .venv

# Activate it on Linux/macOS/WSL
source .venv/bin/activate

# Install packages in it
python -m pip install requests

# Leave it
deactivate
```

By default, a venv does not expose globally installed third-party packages. Avoid `--system-site-packages` unless you specifically need that behavior.

### Check the active environment

```bash
which python
which pip
echo "$VIRTUAL_ENV"
python -c "import sys; print(sys.prefix != sys.base_prefix)"
```

### Good practice

- Use one virtual environment per project.
- Do not commit `.venv/` or other venv directories.
- Prefer `python -m pip` over plain `pip` when interpreter selection matters.
- Recreate package sets with `requirements.txt` when using pip:

```bash
python -m pip freeze > requirements.txt
```

---

## Development checks

```bash
flake8 ex0/construct.py ex1/loading.py ex2/oracle.py
mypy ex0/construct.py ex1/loading.py ex2/oracle.py
```

Exercise 1 may permit import-related lint or type-checking exceptions when third-party dependencies are intentionally missing and handled gracefully.
