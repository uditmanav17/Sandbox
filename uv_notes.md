# UV: The Ultimate Python Project & Package Manager

**References:**
- [Official Documentation](https://docs.astral.sh/uv/)
- [Video Tutorial: Use UV to Replace Pip, Venv & More](https://www.youtube.com/watch?v=AMdG7IjgSPM)

## Overview
**`uv`** is an extremely fast, Rust-based Python package installer and project manager. It unifies the functionality of multiple tools (`pip`, `pip-tools`, `pipx`, `poetry`, `pyenv`, `virtualenv`) into a single, cohesive binary.

**Key Benefits:**
- **Speed**: 10-100x faster than pip.
- **Unified Workflow**: One tool for projects, tools, and python versions.
- **Global Caching**: Saves disk space by sharing packages across environments (via hard links) while keeping environments isolated.
- **Reproducibility**: Automatically manages `uv.lock` for deterministic builds.

---

## 1. Installation

### Windows (PowerShell)
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### macOS / Linux
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
*Also available via Homebrew: `brew install uv`*

---

## 2. Project Management (The "UV Way")
*Best for new projects or modern workflows using `pyproject.toml`.*

### Initialize Project
Sets up project structure (`.python-version`, `pyproject.toml`, `.gitignore`, `hello.py`).
```bash
# Initialize in current directory
uv init

# Initialize a library/application specifically
uv init --app my-app
uv init --lib my-lib

# Initialize with a specific Python version
uv init --python 3.9
```

### Set/Update Python Version
**During Init:**
Pass the `--python` argument as shown above.

**Existing Project:**
To change the Python version for a project already managed by `uv`:
1.  Run `uv python pin` to update the `.python-version` file.
2.  Run `uv sync` to update the virtual environment and lockfile.
```bash
# Switch project to Python 3.11
uv python pin 3.11
uv sync
```

### Dependency Management
`uv` automatically creates/manages the virtual environment (`.venv`) and lockfile (`uv.lock`) when you modify dependencies.

```bash
# Add a dependency (updates pyproject.toml & uv.lock, installs into .venv)
uv add pandas

# Add a development dependency (e.g., testing, linting)
uv add --dev pytest ruff

# Remove a dependency
uv remove pandas
```

### Running Code
Run scripts or commands within the project's environment context. `uv` ensures the environment is up-to-date before running.
```bash
# Run the main script
uv run hello.py

# Run a command (e.g., calling a library)
uv run python -m http.server
```

### Introspection & Sync
```bash
# View dependency tree
uv tree

# Sync environment with lockfile (install/uninstall to match exact state)
uv sync
```

---

## 3. Global Tool Management (Replace `pipx`)
Manage globally installed Python CLIs (like `ruff`, `black`, `yt-dlp`) without polluting your system Python.

### Run Tools Ephemerally (`uvx`)
Download and run a tool temporarily without installing it permanently.
```bash
# Run ruff check on current dir
uvx ruff check .
# OR
uv tool run ruff check .
```

### Install Tools Permanently
```bash
# Install a tool
uv tool install ruff

# List installed tools
uv tool list

# Upgrade all tools
uv tool upgrade --all

# Uninstall a tool
uv tool uninstall ruff
```

---

## 4. Legacy/Scripting Support (Replace `pip` & `venv`)
*For simple scripts or when you need manual control over virtual environments.*

### Manage Virtual Environments
```bash
# Create a venv (defaults to .venv)
uv venv

# Create with specific Python version
uv venv --python 3.10

# Activate
# Windows: .venv\Scripts\activate
# Mac/Linux: source .venv/bin/activate
```

### Pip Interface
`uv pip` commands are drop-in replacements for `pip`, but faster.
```bash
# Install a package
uv pip install numpy

# Install from requirements.txt
uv pip install -r requirements.txt

# Compile requirements (pip-compile replacement)
uv pip compile pyproject.toml -o requirements.txt
```

---

## 5. Python Version Management (Replace `pyenv`)
`uv` can download and manage Python executables itself.

```bash
# Install a specific Python version
uv python install 3.12

# List available versions
uv python list

# Pin project to a specific version
uv python pin 3.11
```

---

## Summary of Commands

| Goal | Old Way | UV Way |
|------|---------|--------|
| **Create Project** | `mkdir` + `touch` | `uv init` |
| **Create Venv** | `python -m venv .venv` | `uv venv` (or handled auto by `uv run`) |
| **Install Pkg** | `pip install pkg` | `uv add pkg` (project) or `uv pip install pkg` (script) |
| **Run Script** | `source .venv/bin/activate && python script.py` | `uv run script.py` |
| **Lock Deps** | `pip freeze > requirements.txt` | `uv.lock` (automatic) |
| **Run Tool** | `pipx run tool` | `uvx tool` |
