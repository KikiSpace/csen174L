# GitHub Actions CI/CD Workflow

This repository uses GitHub Actions for continuous integration and testing.

## Workflows

### CI/CD Pipeline (`ci.yml`)

Automatically runs on:
- Push to `main` or `develop` branches
- Pull requests targeting `main` or `develop` branches

## Jobs

### 1. Test Job
- **Runs on**: Ubuntu latest
- **Node versions**: 18.x and 20.x (matrix strategy)
- **Steps**:
  1. Checkout code
  2. Setup Node.js with caching
  3. Install dependencies with `npm ci`
  4. Run unit tests (mock-based, free)
  5. Generate coverage report (Node 20.x only)
  6. Upload coverage to Codecov (optional)

### 2. Code Quality Check
- **Runs on**: Ubuntu latest
- **Node version**: 20.x
- **Steps**:
  1. Checkout code
  2. Setup Node.js
  3. Install dependencies
  4. Run security audit (`npm audit`)

### 3. Integration Tests (Manual Trigger)
- **Runs on**: Ubuntu latest (when triggered)
- **Trigger**: Include `[integration]` in commit message
- **Steps**:
  1. Checkout code
  2. Setup Node.js
  3. Install dependencies
  4. Run integration tests with real OpenAI API

## Setup Instructions

### 1. Enable GitHub Actions
GitHub Actions is enabled by default for public repositories. For private repositories, go to Settings → Actions → General and enable actions.

### 2. Configure Secrets (Optional)

#### For Integration Tests (Optional)
If you want to run integration tests with real API calls:

1. Go to your repository on GitHub
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add the following secret:
   - Name: `OPENAI_API_KEY`
   - Value: Your OpenAI API key

**Note**: Integration tests cost money (~$0.10 per run) and only run when you include `[integration]` in your commit message.

#### For Code Coverage (Optional)
To upload coverage reports to Codecov:

1. Sign up at [codecov.io](https://codecov.io)
2. Add your repository
3. Get your Codecov token
4. Add it as a repository secret:
   - Name: `CODECOV_TOKEN`
   - Value: Your Codecov token

### 3. Branch Protection Rules (Recommended)

To ensure code quality, set up branch protection:

1. Go to **Settings** → **Branches**
2. Click **Add rule** for `main` branch
3. Enable:
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging
   - Select status checks: `Run Tests`
4. Save changes

## Usage

### Regular Development
Just push code or create a pull request normally:

```bash
git add .
git commit -m "Add new feature"
git push origin main
```

The workflow will automatically:
- Run unit tests on Node 18.x and 20.x
- Generate coverage report
- Check for security vulnerabilities

### Running Integration Tests
To trigger integration tests with real API (costs money):

```bash
git add .
git commit -m "Add new feature [integration]"
git push origin main
```

**Warning**: This will make real API calls to OpenAI and incur costs (~$0.10).

## Viewing Results

### On GitHub
1. Go to your repository
2. Click the **Actions** tab
3. Select a workflow run to see details

### Status Badges
Add this badge to your README.md to show build status:

```markdown
![CI/CD Pipeline](https://github.com/YOUR_USERNAME/YOUR_REPO/actions/workflows/ci.yml/badge.svg)
```

Replace `YOUR_USERNAME` and `YOUR_REPO` with your GitHub username and repository name.

## Workflow Features

### Fast Feedback
- Uses `npm ci` for faster, more reliable installs
- Caches npm dependencies between runs
- Runs unit tests (fast, free) by default

### Cost Optimization
- Unit tests (mock-based) run on every commit (free)
- Integration tests (real API) only run when explicitly triggered
- Prevents accidental API costs

### Multi-Version Testing
- Tests on Node.js 18.x and 20.x
- Ensures compatibility across versions

### Security
- Runs `npm audit` to check for vulnerabilities
- Continues even if non-critical issues found

## Customization

### Change Node Versions
Edit `.github/workflows/ci.yml`:

```yaml
strategy:
  matrix:
    node-version: [16.x, 18.x, 20.x]  # Add or remove versions
```

### Change Trigger Branches
Edit the `on` section:

```yaml
on:
  push:
    branches: [ main, develop, staging ]  # Add your branches
  pull_request:
    branches: [ main ]
```

### Add More Jobs
Add new jobs to the workflow file:

```yaml
jobs:
  test:
    # ... existing job

  deploy:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: test  # Wait for tests to pass
    if: github.ref == 'refs/heads/main'
    steps:
      # ... deployment steps
```

## Troubleshooting

### Tests Failing
1. Check the Actions tab for detailed logs
2. Reproduce locally: `npm run test:unit`
3. Fix issues and push again

### Workflow Not Running
1. Check that the workflow file is in `.github/workflows/`
2. Verify the file name ends with `.yml` or `.yaml`
3. Check branch names match the trigger configuration

### Integration Tests Not Running
1. Ensure commit message includes `[integration]`
2. Verify `OPENAI_API_KEY` secret is set
3. Check Actions tab for detailed error logs

## Best Practices

1. **Always run tests locally first**: `npm test`
2. **Use unit tests for regular development**: Fast and free
3. **Use integration tests sparingly**: Only before major releases
4. **Keep dependencies updated**: Run `npm audit` regularly
5. **Review workflow logs**: Check for warnings and optimize

## Cost Considerations

- **Unit tests**: Free (uses mocks)
- **Integration tests**: ~$0.10 per run (real API calls)
- **GitHub Actions**: 2,000 minutes/month free for public repos

To minimize costs:
- Use unit tests for all regular development
- Only use `[integration]` tag before releases
- Consider running integration tests manually instead

## Support

For issues with GitHub Actions:
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Actions Community](https://github.community/c/code-to-cloud/52)

For issues with this project:
- Check the main README.md
- Review workflow logs in Actions tab
