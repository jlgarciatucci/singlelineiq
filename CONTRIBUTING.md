# Contributing to SingleLineIQ

Thank you for your interest in contributing to SingleLineIQ! This guide outlines the development standards, code style, and submission flows to ensure a smooth contribution process.

---

## Code of Conduct

All contributors are expected to maintain a professional, respectful, and collaborative environment.

---

## Development Workflow

1. **Fork and Clone**: Fork the repository on GitHub and clone it locally.
2. **Branching**: Create a descriptive feature branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Install Dependencies**:
   - For backend (Python 3.10+):
     ```bash
     cd backend
     python -m venv .venv
     # Activate and install
     pip install -r requirements.txt
     ```
   - For frontend (Next.js / Node.js 18+):
     ```bash
     cd frontend
     npm install
     ```
4. **Develop & Test**: Keep your changes modular and make sure to add/run tests before committing!
5. **Commit Messages**: Write clear, imperative commits:
   ```text
   feat: add voltage mismatch verification check
   fix: adjust report margin layout spacing
   docs: update setup steps in README
   ```

---

## Code Style Conventions

To keep the codebase uniform and readable, we adhere to the following formatting standards:

### Backend (Python)
- **Style Rules**: Follow PEP 8 guidelines.
- **Type Annotations**: Use Python type hints where possible to catch structural issues early.
- **Docstrings**: Provide descriptive docstrings for public classes and functions.

### Frontend (Next.js / TypeScript)
- **Formatting**: Adhere to ESLint and Prettier rules.
- **Design Guidelines**: Follow responsive layouts and dark-mode styling tokens. Keep styles modular and clean.

---

## Running Tests

Before submitting a Pull Request, ensure that all tests run and pass cleanly:

### Backend Tests
From the `backend` directory, execute:
```bash
.venv/Scripts/pytest
```

---

## Pull Request Guidelines

1. **Keep it Small**: Focus each PR on resolving a single issue or implementing one specific feature.
2. **Pass Tests**: Do not submit PRs with failing unit tests or typescript build compilation errors.
3. **Sync with Main**: Pull latest changes from upstream `main` and resolve any merge conflicts before submitting.
4. **Document**: If introducing a new CLI option, API endpoint, or configuration, document it in the README.
