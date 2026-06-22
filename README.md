# Railway Management System

Backend project for managing railway operations.

---

# Install uv (Required)

This project uses **uv** for dependency management and running tools.

## Linux / macOS

If you have **curl**:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

If you do **not** have curl:

```bash
wget -qO- https://astral.sh/uv/install.sh | sh
```

## Windows (PowerShell)

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## Alternative: Install with pip

```bash
pip install uv
```

If installed with pip, you can still run the same commands:

```bash
python -m uv sync --group dev
python -m uv run pre-commit install
```

## Verify Installation

```bash
uv --version
```

If the command is not found, restart your **terminal/shell** so the uv path is added to your environment.

Once `uv --version` works, continue to the next step.

---

# Getting Started

Run the following commands:

```bash
git clone https://github.com/QB12-Group1/railway-management-system.git
cd railway-management-system
uv sync --group dev
uv run pre-commit install
git checkout dev
git pull origin dev
git checkout -b feature/<your-name>
```

Example:

```bash
git checkout -b feature/ali
```

---

# Working on the Project

After making changes:

```bash
git add .
git commit -m "describe your change"
git push
```

Then open a **Pull Request**:

```
feature/... → dev
```

Your code will be reviewed before merging.

---

# Updating Your Branch with Latest dev

Before opening or updating a PR:

```bash
git checkout dev
git pull origin dev
git checkout feature/<your-branch>
git merge dev
```

Resolve conflicts if needed and push again.

---

## Code Quality Checks (Pre-commit)

This repository uses **pre-commit hooks** to automatically check code quality before every commit.

The following tools run automatically:

- **Ruff** – linting and formatting
- **Pyright** – static type checking
- **pre-commit hooks** – whitespace fixes and file checks

Because of this setup, **you cannot successfully create a commit if there are linting or type errors**.

When you run:

```bash
git commit -m "your message"
```

pre-commit will automatically run all checks.

### What you should do

If a check fails:

1. Read the output printed in the terminal.
2. Fix the issue the tool is pointing out.
3. Stage the changes again.
4. Commit again.

Example workflow:

```bash
git add .
git commit -m "add train scheduling logic"
```

If Ruff automatically fixes issues, you may need to stage the changes again:

```bash
git add .
git commit -m "add train scheduling logic"
```

### Running checks manually

You can run all checks manually with:

```bash
uv run pre-commit run --all-files
```

This is useful before pushing large changes.

### Important

Please make sure:

- Your code passes **linting**
- Your code passes **type checking**
- There are **no errors reported by pre-commit**

Commits that fail these checks will be blocked until the issues are resolved.
