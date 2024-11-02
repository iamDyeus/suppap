# Contributing to Suppap

First off, thanks for taking the time to contribute! 🎉

Suppap is all about fun and surprise, and we're excited to have you join in on making it even better! Whether you're fixing bugs, adding new features, or improving documentation, your contributions are welcome.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [I Have a Question](#i-have-a-question)
- [I Want To Contribute](#i-want-to-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Your First Code Contribution](#your-first-code-contribution)
  - [Improving The Documentation](#improving-the-documentation)
- [Styleguides](#styleguides)
  - [Git Commit Messages](#git-commit-messages)
  - [Python Styleguide](#python-styleguide)
- [Testing](#testing)
- [Join The Project Team](#join-the-project-team)

## Code of Conduct

This project and everyone participating in it is governed by the [Suppap Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to [project email].

## I Have a Question

If you have a question, please check the following resources first:

1. [README.md](README.md)
2. [Existing Issues](https://github.com/iamDyeus/suppap/issues)

If you still need clarification, feel free to open a new issue with the "question" label.

## I Want To Contribute

### Reporting Bugs

Before submitting a bug report:

1. Update to the latest version of Suppap.
2. Check if the bug has already been reported in the [issue tracker](https://github.com/iamDyeus/suppap/issues).
3. Collect information about the bug (OS, Python version, steps to reproduce, etc.).

To submit a bug report, create a new issue using the bug report template. Provide as much relevant information as possible.

### Suggesting Enhancements

We love new ideas! Before submitting an enhancement suggestion:

1. Check if the enhancement has already been suggested in the [issue tracker](https://github.com/iamDyeus/suppap/issues).
2. Consider if your idea fits within the scope and goals of Suppap.

To submit an enhancement suggestion, create a new issue using the feature request template. Be clear and provide detailed explanations of the proposed feature.

### Your First Code Contribution

Unsure where to begin? Look for issues labeled "good first issue" or "help wanted".

To set up your development environment:

1. Fork the repository.
2. Clone your fork: `git clone https://github.com/your-username/suppap.git`
3. Create a new branch: `git checkout -b my-branch-name`
4. Install dependencies: `pip install -r requirements.txt`
5. Make your changes and test thoroughly.
6. Commit your changes: `git commit -m "Add a descriptive commit message"`
7. Push to your fork: `git push origin my-branch-name`
8. Create a pull request.

### Improving The Documentation

Good documentation is crucial! If you find any part of our documentation unclear or incomplete, please help us improve it. This includes the README, inline code comments, and this CONTRIBUTING.md file.

## Styleguides

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

### Python Styleguide

We follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide for Python code. Additionally:

- Use 4 spaces for indentation (not tabs)
- Use docstrings for functions and classes
- Keep lines to a maximum of 79 characters
- Use meaningful variable names

## Testing

### Running Tests

Before submitting your changes, please make sure all tests pass. We use `pytest` with `pytest-cov` for coverage. Follow these steps to run the tests:

1. **Set up the testing environment** by installing required packages:
   ```bash
   pip install -r requirements.txt
    ```
2. **Run all the tests**:
    ```bash
    pytest --cov=src tests/
    ```
3. **Run specific tests**:
    ```bash
    pytest tests/test_<file_name>.py
    ```
This is helpful for testing only the functionality you changed.

### Writing Tests

When adding new features or modifying existing functionality, please write or update tests to ensure code quality and prevent future regressions. We use unittest along with pytest for running tests.

- Place test files in the tests/ directory and name them following the pattern `test_<module_name>.py`.
- Use descriptive function names for tests. For example, `test_change_wallpaper_success` clearly indicates what the test checks.
- Mock external dependencies (like network calls) using `unittest.mock` to avoid dependencies on external services.
- Ensure tests are deterministic and can run independently of each other.


For more information on writing tests, see the [pytest documentation](https://docs.pytest.org/en/stable/) and the [unittest documentation](https://docs.python.org/3/library/unittest.html).

## Join The Project Team

Interested in becoming a core contributor? Start by making consistent contributions and engaging with the community. We'll reach out if we think you'd be a good fit for the team!

Remember, Suppap is all about having fun and surprising people with cool wallpapers. Let's keep that spirit in our contributions too! 🎨🖼️
