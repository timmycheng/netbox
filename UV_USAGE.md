# Using UV with NetBox

This project has been configured to use [uv](https://github.com/astral-sh/uv) as the Python package manager.

## What is UV?

uv is a fast Python package installer and resolver, written in Rust. It's designed to be a drop-in replacement for pip and pip-tools.

## Setup

### Prerequisites
- Python 3.10 or higher
- uv installed (https://github.com/astral-sh/uv#installation)

### Installation

1. **Install dependencies:**
   ```bash
   uv sync
   ```
   This will create a virtual environment in `.venv/` and install all dependencies from `uv.lock`.

2. **Activate the virtual environment:**
   ```bash
   # On Windows
   .venv\Scripts\activate
   
   # On Unix/macOS
   source .venv/bin/activate
   ```

3. **Run commands in the virtual environment:**
   ```bash
   uv run python manage.py runserver
   ```

## Common Commands

- **Install a new dependency:**
  ```bash
  uv add package-name
  ```

- **Install a development dependency:**
  ```bash
  uv add --dev package-name
  ```

- **Remove a dependency:**
  ```bash
  uv remove package-name
  ```

- **Update dependencies:**
  ```bash
  uv lock --upgrade
  uv sync
  ```

- **Run a command in the virtual environment:**
  ```bash
  uv run python manage.py migrate
  uv run python manage.py collectstatic
  ```

## Files

- `pyproject.toml` - Project configuration and dependencies
- `uv.lock` - Locked dependency versions (similar to pip's requirements.lock)
- `.venv/` - Virtual environment directory (auto-created)

## Migration from requirements.txt

The original `requirements.txt` has been migrated to the `dependencies` section in `pyproject.toml`. The `uv.lock` file ensures reproducible installations across different environments.

## Benefits of UV

- **Speed**: Much faster than pip for dependency resolution and installation
- **Reliability**: Deterministic dependency resolution
- **Compatibility**: Drop-in replacement for pip workflows
- **Modern**: Uses pyproject.toml standard for Python packaging