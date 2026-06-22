# Railway Management System

Terminal project for managing railway operations.

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

```bash
git clone https://github.com/QB12-Group1/railway-management-system.git
cd railway-management-system
uv sync --group dev
uv run pre-commit install
```

---

# Working on a Task / Feature

All development happens on **feature branches created from `dev`**.

Branch format:

```
feature/<your-name>/<task-name>
```

Example:

```
feature/ali/implement-railway-model
feature/ilia/implement-train-model
```

---

## Step‑by‑Step Workflow

### 1. Checkout `dev` and pull the latest updates

Always start from the latest version of `dev`.

```bash
git checkout dev
git pull origin dev
```

---

### 2. Create your feature branch

Create a new branch for your assigned task.

```bash
git checkout -b feature/<your-name>/<task-name>
```

Example:

```bash
git checkout -b feature/ilia/implement-train-model
```

Each branch should represent **one task or feature**.

---

### 3. Start working on your task

Make the changes needed for your feature or bug fix.

---

### 4. Add your changes

Stage the files you modified.

```bash
git add .
```

---

### 5. Commit your changes

```bash
git commit -m "describe your change"
```

Example:

```bash
git commit -m "Implement Train Model"
```

---

### 6. Push your branch

Push your feature branch to GitHub.

```bash
git push -u origin feature/<your-name>/<task-name>
```

Example:

```bash
git push -u origin feature/ilia/implement-train-model
```

---

### 7. Open a Pull Request

Open a PR on GitHub:

```
feature/<your-name>/<task-name> → dev
```

Your code will be reviewed before merging.

After the PR is merged, the feature branch will be deleted.

---

# Keeping Your Branch Updated

If `dev` changes while you are working, update your branch.

```bash
git checkout dev
git pull origin dev
git checkout feature/<your-name>/<task-name>
git merge dev
```

Resolve conflicts if necessary, then push again.

---

# Code Quality Checks (Pre-commit)

This repository uses **pre-commit hooks** to automatically check code quality before every commit.

Tools used:

- **Ruff** – linting and formatting
- **Pyright** – static type checking
- **pre-commit hooks** – whitespace fixes and file checks

If checks fail:

1. Read the error output
2. Fix the issue
3. Stage the changes again
4. Commit again

Example:

```bash
git add .
git commit -m "add train scheduling logic"
```

If Ruff auto-fixes files you may need to stage again:

```bash
git add .
git commit -m "add train scheduling logic"
```

Run checks manually:

```bash
uv run pre-commit run --all-files
```

Make sure your code passes all checks before pushing.
