# Contributing to Sjenk

Thank you for considering contributing to Sjenk! We welcome contributions from the community and are excited to see what you will bring to the project.

## How to Contribute

### Reporting Bugs

If you find a bug, please report it by creating an issue on our [GitHub Issues](https://github.com/lewiuberg/sjenk/issues) page. Provide as much detail as possible, including steps to reproduce the bug, the expected behavior, and the actual behavior.

### Suggesting Features

We welcome feature suggestions! Please create an issue on our [GitHub Issues](https://github.com/lewiuberg/sjenk/issues) page and describe the feature you would like to see, why you think it would be useful, and how it should work.

### Submitting Pull Requests

1. **Fork the Repository**: Click the "Fork" button on the top right of the repository page to create a copy of the repository on your GitHub account.

2. **Clone the Repository**: Clone your forked repository to your local machine.

   ```sh
   git clone https://github.com/your-username/sjenk.git
   cd sjenk
   git switch dev
   ```

   or if you are using GitHub CLI:

   ```sh
   gh repo clone your-username/sjenk
   cd sjenk
   git switch dev
   ```

3. **Create a Branch**: Create a new branch for your feature or bugfix.

   For new features:

   ```sh
   git switch -c feature/feature-name
   ```

   For bugfixes:

   ```sh
   git switch -c bugfix/bugfix-name
   ```

4. **Make Changes**: Make your changes to the codebase. Ensure that your code follows the project's coding standards and includes appropriate tests.

5. **Commit Changes**: Commit your changes with a clear and descriptive commit message.

   ```sh
   git commit -m "Description of the changes in imperative mood"
   ```

   Example:

   ```sh
   git commit -m "Refactor SQLModel to use Pydantic BaseModel"
   ```

   or

   ```sh
   git commit -m "Add tests for the new feature"
   ```

6. **Push Changes**: Push your changes to your forked repository.

   ```sh
   git push origin feature/feature-name
   ```

7. **Create a Pull Request**: Go to the original repository and create a pull request from your forked repository. Provide a clear description of the changes you have made and any relevant information.

### Code Style

Please ensure that your code adheres to the project's coding standards. We use [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code. You can use tools like `ruff` and `uv` to check your code for style issues.

### Running Tests

Before submitting your pull request, make sure that all tests pass. You can run the tests using the following command:

```sh
pytest
```

## Code of Conduct

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project, you agree to abide by its terms.

Thank you for contributing!
