# Real API Testing Guide

## Overview

This project supports **two types of tests**:

1. **Unit Tests with Mocks** - Fast, free, no API keys needed
2. **Integration Tests with Real APIs** - Slower, costs money, requires API keys

## Test Types Comparison

| Feature | Unit Tests (Mock) | Integration Tests (Real API) |
|---------|------------------|------------------------------|
| **Speed** | ⚡ Fast (~1 second) | 🐌 Slow (~30-90 seconds) |
| **Cost** | 💚 Free | 💰 Costs money (~$0.05 per test run) |
| **API Keys** | ✅ Not required | ⚠️ Required (OPENAI_API_KEY) |
| **Network** | ✅ Works offline | ❌ Requires internet |
| **Reliability** | ✅ Always consistent | ⚠️ Can fail due to rate limits |
| **Use Case** | Development, CI/CD | Pre-deployment validation |
| **File** | `ai-behavior.test.js` | `ai-behavior-real-api.test.js` |

## Running Tests

### Quick Reference

```bash
# Run only unit tests (with mocks) - DEFAULT
npm test
# or
npm run test:unit

# Run only integration tests (with real API) - COSTS MONEY
npm run test:integration

# Run all tests (unit + integration)
npm run test:all

# Watch mode (unit tests only)
npm run test:watch
```

### Detailed Commands

#### 1. Unit Tests (Mock) - Recommended for Development

```bash
# Run all unit tests
npm test

# Run unit tests in watch mode
npm run test:watch

# Run specific mock test file
npm test -- ai-behavior.test.js

# Run with coverage
npm run test:coverage
```

**Characteristics:**
- ✅ Runs in < 1 second
- ✅ No API costs
- ✅ Works without API keys
- ✅ Perfect for TDD workflow
- ✅ Safe for CI/CD

#### 2. Integration Tests (Real API) - Use Before Deployment

```bash
# Run integration tests
npm run test:integration

# Run integration tests in watch mode
npm run test:integration -- --watch

# Run specific integration test
npm test -- ai-behavior-real-api.test.js
```

**Characteristics:**
- ⏱️ Takes 30-90 seconds
- 💰 Costs ~$0.05 per full run
- 🔑 Requires OPENAI_API_KEY
- 🌐 Requires internet connection
- ✅ Validates real API behavior

## Setup for Real API Tests

### 1. Set API Key

Make sure your `.env` file has your OpenAI API key:

```bash
OPENAI_API_KEY=sk-proj-your-actual-api-key-here
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Run Integration Tests

```bash
npm run test:integration
```

## When to Use Each Type

### Use Unit Tests (Mock) When:

✅ **During Development**
- Writing new features (TDD)
- Refactoring code
- Quick feedback loops
- Every commit/push

✅ **In CI/CD Pipelines**
- Automated testing on every PR
- Pre-merge validation
- Fast feedback required

✅ **For Test Coverage**
- Measuring code coverage
- Testing edge cases
- Testing error scenarios

### Use Integration Tests (Real API) When:

✅ **Before Deployment**
- Final validation before releasing
- Confirming API compatibility
- Testing production-like scenarios

✅ **After API Changes**
- OpenAI updates their API
- Testing new models
- Validating prompt changes

✅ **Investigating Issues**
- Debugging real API behavior
- Testing rate limits
- Validating actual responses

## Test Files

### Unit Tests: `ai-behavior.test.js`

```javascript
const { createMockOpenAI } = require('./helpers/mockOpenAI');

test('should generate valid story', async () => {
  const mockClient = createMockOpenAI(); // No real API call
  const response = await mockClient.chat.completions.create({...});
  // Fast, predictable, free
});
```

**Features:**
- 37 tests covering all AI behavior
- Uses mock responses
- Tests JSON parsing, validation, error handling
- Runs in < 1 second

### Integration Tests: `ai-behavior-real-api.test.js`

```javascript
const OpenAI = require('openai');

test('should generate valid story with real API', async () => {
  const openai = new OpenAI({...}); // Real OpenAI client
  const response = await openai.chat.completions.create({...});
  // Real API call, real response, real cost
});
```

**Features:**
- 7 comprehensive integration tests
- Tests GPT-4 real responses
- Tests DALL-E image generation
- Tests full end-to-end workflow
- Validates vintage anime style in prompts
- Tests error handling with real API

## Integration Test Details

### Tests Included

1. **GPT-4 Real API Tests**
   - ✅ Generate valid story data
   - ✅ Include vintage anime style keywords
   - ✅ Generate coherent story continuations

2. **DALL-E 3 Real API Tests**
   - ✅ Generate actual anime images
   - ✅ Return valid image URLs

3. **Full Workflow Tests**
   - ✅ Complete scene generation (GPT-4 + DALL-E)
   - ✅ End-to-end integration

4. **Error Handling Tests**
   - ✅ Invalid model names
   - ✅ Empty prompts

### Example Output

When you run integration tests, you'll see:

```bash
$ npm run test:integration

⚠️  Running REAL API tests - this will cost money!

Real API Integration Tests
  GPT-4 Real API
    📝 GPT-4 Response: {
      "imagePrompt": "A young warrior in classic 1980s anime style...",
      "narrative": "In the depths of the temple...",
      "nextSuggestion": "The sword begins to glow..."
    }
    ✓ should generate valid story data with real GPT-4 (2431ms)

    🎨 Image Prompt: Vintage 1980s anime style warrior...
    ✓ should include vintage anime style in prompts (1823ms)

  DALL-E 3 Real API
    🖼️  Generated Image URL: https://oaidalleapiprodscus.blob...
    📝 Revised Prompt: A young anime warrior with...
    ✓ should generate real anime image with DALL-E 3 (12156ms)

  Full End-to-End Workflow
    🚀 Starting full workflow test...
    📝 Step 1: Generating story with GPT-4...
    ✅ Story generated
    🎨 Step 2: Generating image with DALL-E...
    ✅ Image generated
    ✓ should complete full scene generation workflow (15234ms)

Tests: 7 passed, 7 total
Time: 32.145s
```

## Cost Estimation

### Per Test Run (Integration Tests)

- **GPT-4o calls**: 3-4 calls × $0.005 = ~$0.015-$0.02
- **DALL-E 3 images**: 2 images × $0.04 = ~$0.08
- **Total per run**: ~$0.10

### Optimization Tips

1. **Run selectively**:
   ```bash
   # Run only one test
   npm run test:integration -- -t "should generate valid story"
   ```

2. **Skip during development**:
   ```bash
   # Set environment variable to skip
   export SKIP_INTEGRATION_TESTS=true
   npm test
   ```

3. **Use smaller models**:
   ```javascript
   model: 'gpt-3.5-turbo' // Instead of gpt-4o
   ```

## Skipping Integration Tests

Integration tests are **automatically skipped** if:

1. No `OPENAI_API_KEY` in environment
2. `SKIP_INTEGRATION_TESTS=true` is set

You'll see:
```
⚠️  Integration tests skipped
To run these tests:
1. Set OPENAI_API_KEY in your .env file
2. Run: npm run test:integration
```

## CI/CD Configuration

### GitHub Actions Example

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
      - run: npm install
      - run: npm run test:unit  # Only unit tests in CI

  integration-tests:
    runs-on: ubuntu-latest
    # Only run on main branch
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
      - run: npm install
      - run: npm run test:integration
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
```

## Best Practices

### Development Workflow

1. **Write tests first (TDD)**:
   ```bash
   npm run test:watch  # Use unit tests
   ```

2. **Develop with mocks**:
   - Fast iteration
   - No API costs
   - Reliable results

3. **Validate with real API before deploy**:
   ```bash
   npm run test:integration
   ```

### Testing Strategy

```
Development Phase:
  └─> Unit Tests (Mock) ✅ Run continuously

Pre-Deployment:
  └─> Integration Tests (Real API) ✅ Run once

Production:
  └─> Unit Tests (Mock) ✅ CI/CD automation
  └─> Integration Tests (Real API) ⚠️ Weekly/Monthly
```

## Troubleshooting

### Integration Tests Not Running

**Problem**: Tests are skipped
```
⚠️  Integration tests skipped
```

**Solution**: Check API key
```bash
# Verify .env file
cat .env | grep OPENAI_API_KEY

# Or set temporarily
OPENAI_API_KEY=your-key npm run test:integration
```

### Rate Limit Errors

**Problem**: `429 Rate Limit Exceeded`

**Solution**: Wait and retry
```bash
# Wait 60 seconds and retry
sleep 60 && npm run test:integration
```

### Timeout Errors

**Problem**: Test timeout after 5000ms

**Solution**: Already configured with longer timeouts
- GPT-4 tests: 30 seconds
- DALL-E tests: 60 seconds
- Full workflow: 90 seconds

### High Costs

**Problem**: Tests are expensive

**Solutions**:
1. Run integration tests less frequently
2. Use `test:unit` for daily development
3. Only run full `test:integration` before releases
4. Use environment variable to skip:
   ```bash
   SKIP_INTEGRATION_TESTS=true npm test
   ```

## Examples

### Running Specific Integration Test

```bash
# Only test GPT-4
npm run test:integration -- -t "GPT-4"

# Only test DALL-E
npm run test:integration -- -t "DALL-E"

# Only test full workflow
npm run test:integration -- -t "Full End-to-End"
```

### Debugging Real API Responses

Integration tests log actual API responses:

```javascript
test('should generate valid story', async () => {
  const response = await openai.chat.completions.create({...});
  const data = JSON.parse(response.choices[0].message.content);

  console.log('\n📝 GPT-4 Response:', JSON.stringify(data, null, 2));
  // See actual API response in test output
});
```

### Comparing Mock vs Real

```bash
# Run both and compare
npm run test:unit -- ai-behavior.test.js
npm run test:integration -- ai-behavior-real-api.test.js
```

## Summary

| Command | Use Case | Speed | Cost |
|---------|----------|-------|------|
| `npm test` | Daily development | ⚡ Fast | 💚 Free |
| `npm run test:unit` | TDD, CI/CD | ⚡ Fast | 💚 Free |
| `npm run test:integration` | Pre-deployment | 🐌 Slow | 💰 ~$0.10 |
| `npm run test:all` | Full validation | 🐌 Slow | 💰 ~$0.10 |

**Recommendation**: Use **unit tests** for development, **integration tests** before deployment.

---

**Need help?** See also:
- [TEST_GUIDE.md](TEST_GUIDE.md) - General testing guide
- [TDD_WORKFLOW.md](TDD_WORKFLOW.md) - TDD workflow
- [TESTING_SUMMARY.md](TESTING_SUMMARY.md) - Testing overview
