# QA Automation Project

Automated UI tests for Saucedemo e-commerce site using Playwright and Pytest, with Jira integration for test case management.

## Features

- Automated UI testing using Playwright
- Jira integration for test case tracking
- Automatic test result updates in Jira
- Screenshot capture for test evidence
- Performance metrics tracking

## Prerequisites

- Python 3.12 or higher
- Conda/Mamba environment
- Jira account with API access
- Chrome/Chromium browser

## Setup

1. Create and activate conda environment:

   ```powershell
   conda create -n joy python=3.12
   conda activate joy
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Install browsers:

   ```bash
   playwright install
   ```

4. Configure Jira integration:
   ```powershell
   $env:JIRA_USERNAME='your-jira-email@example.com'
   $env:JIRA_TOKEN='your-jira-api-token'
   ```

## Tests

- `test_login.py`:

  - Tests successful login with valid credentials
  - Tests error handling with invalid credentials
  - Screenshots captured for verification

- `test_cart.py`:

  - Tests adding items to cart
  - Validates cart badge count
  - Measures page load performance

- `test_checkout.py`:
  - Tests complete checkout flow
  - Validates form submission
  - Confirms order completion

## Running Tests

Run all tests:

```bash
pytest -v
```

Run with detailed output:

```bash
pytest -v -s
```

Run specific test file:

```bash
pytest test_login.py -v
```

## Jira Integration

1. Create these issues in your Jira project:

   - TEST-1: Test the complete checkout flow
   - TEST-2: Test successful login flow
   - TEST-3: Test invalid login error handling

2. Test results will automatically:
   - Update corresponding Jira issues
   - Add detailed test execution comments
   - Include timestamps and duration
   - Report any failures with error details

## Project Structure

```
├── test_login.py       # Login test scenarios
├── test_cart.py        # Shopping cart tests
├── test_checkout.py    # Checkout process tests
├── jira_integration.py # Jira integration utilities
├── requirements.txt    # Project dependencies
├── README.md          # Project documentation
└── workflows/         # CI/CD workflows
    └── ci.yml        # GitHub Actions CI configuration
```

## Continuous Integration

This project uses GitHub Actions for continuous integration. The workflow is defined in `.github/workflows/ci.yml`:

```yaml
name: CI
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with: { python-version: '3.9' }
      - run: pip install playwright pytest
      - run: playwright install
      - run: pytest
```

The CI workflow:

- Triggers on every push to the repository
- Sets up Python 3.9 environment
- Installs required dependencies
- Installs Playwright browsers
- Runs all tests automatically

### CI Status

[![CI Status](https://github.com/joypciu/playwright_test/actions/workflows/ci.yml/badge.svg)](https://github.com/joypciu/playwright_test/actions)

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
