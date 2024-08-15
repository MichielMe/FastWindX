# Continuous Integration

## Formatting

### [Black](<https://black.readthedocs.io/en/stable/>)

Black is a code formatter that will format your code to be PEP8 compliant.

## Linting

### [Pylint](<https://pylint.pycqa.org/en/latest/>)

Pylint is a linter that will check your code for errors and enforce a coding standard.

### [Flake8](<https://flake8.pycqa.org/en/latest/>)

Flake8 is a linter that will check your code for errors and enforce a coding standard.

### [ruffus](<http://www.ruffus.org.uk/>)

Ruffus is a linter that will check your code for errors and enforce a coding standard.

## Code Metrics

### [Radon](<https://radon.readthedocs.io/en/latest/>)

Radon is a code metrics tool that will check your code for complexity and maintainability.

Examples:

```bash
radon cc -a -nb app
radon mi app
```

This will check the code complexity and maintainability of the code in the `app` directory.

### [Xenon](<https://xenon.readthedocs.io/en/latest/>)

Xenon is a code metrics tool that will check your code for complexity and maintainability.

## Typing

### [Mypy](<https://mypy.readthedocs.io/en/stable/>)

Mypy is a static type checker that will check your code for type errors.

Examples:

```bash
mypy app
```

This will check the code in the `app` directory for type errors.

## Security

### [Bandit](<https://bandit.readthedocs.io/en/latest/>)

Bandit is a security linter that will check your code for security vulnerabilities.

Examples:

```bash
bandit -r app
```

This will check the code in the `app` directory for security vulnerabilities.
