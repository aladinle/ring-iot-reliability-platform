# Automation Workflow

This project uses two layers of automation:

1. Local PowerShell scripts for fast developer validation.
2. GitHub Actions for repository-level CI gates.

GitHub Copilot can help create changes or work from issues, but GitHub Actions should decide whether code is safe to merge or deploy.

## Local Test Command

```powershell
.\scripts\test_all.ps1
```

This runs:

- C++ CMake build and CTest.
- Python backend tests.

## Local Commit And Push Command

```powershell
.\scripts\commit_if_tests_pass.ps1 -Message "chore: initialize project foundation"
```

This script:

- Checks for local changes.
- Runs all tests.
- Stages files only after tests pass.
- Creates a commit.
- Pushes the current branch to `origin`.

## GitHub Actions CI

The workflow at `.github/workflows/ci.yml` runs on:

- Pull requests to `main`.
- Pushes to `main`.
- Pushes to `codex/**` branches.

It validates:

- C++ build and tests.
- Backend Python tests.

## Deployment

Deployment is intentionally a placeholder until a real target exists. Once a target is chosen, the `deploy-placeholder` job can be replaced with Docker publish, cloud deployment, or server update steps.

Avoid deploying directly from unreviewed AI-generated changes. Prefer:

```text
Copilot or developer changes -> pull request -> CI passes -> review -> merge -> deploy from main
```

