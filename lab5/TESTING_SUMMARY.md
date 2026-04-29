# Testing Setup Summary

## What Was Created

A comprehensive Test-Driven Development (TDD) framework has been set up for your Anime Story Generator project.

### Files Created

```
lab5/
├── package.json                      # Updated with Jest and test scripts
├── .gitignore                        # Updated to exclude coverage reports
├── TEST_GUIDE.md                     # Complete testing guide (11KB)
├── TDD_WORKFLOW.md                   # TDD workflow tutorial (9KB)
├── TESTING_SUMMARY.md                # This file
├── README.md                         # Updated with testing section
└── __tests__/                        # Test directory
    ├── helpers/
    │   ├── mockData.js              # Sample test data and scenarios
    │   └── mockOpenAI.js            # Mock OpenAI client for testing
    ├── ai-behavior.test.js          # AI response behavior tests
    ├── api.test.js                  # API endpoint tests
    └── template.test.js             # Template for creating new tests
```

## Test Framework

**Testing Library:** Jest v29.7.0
**HTTP Testing:** Supertest v6.3.3

### Available Test Commands

```bash
# Unit Tests (Mock - Fast, Free)
npm test              # Run all tests once
npm run test:watch    # Run tests in watch mode (auto-rerun)
npm run test:coverage # Run tests with coverage report
npm run test:unit     # Run only unit tests (with mocks)

# Integration Tests (Real API - Slow, Costs Money)
npm run test:integration  # Run tests with REAL OpenAI API
npm run test:all          # Run both unit and integration tests
```

## Test Types

### Unit Tests (Mock) - Default
- ⚡ **Fast**: ~1 second
- 💚 **Free**: No API costs
- ✅ **No API Keys**: Works without OPENAI_API_KEY
- 📂 **Files**: `ai-behavior.test.js`, `api.test.js`

### Integration Tests (Real API) - Optional
- 🐌 **Slow**: ~30-90 seconds
- 💰 **Costs**: ~$0.10 per run
- 🔑 **API Keys**: Requires OPENAI_API_KEY
- 📂 **File**: `ai-behavior-real-api.test.js`
- 📖 **Guide**: See [REAL_API_TESTING.md](REAL_API_TESTING.md)

## What You Can Test

### 1. AI Behavior Tests (`ai-behavior.test.js`)

Tests for AI response generation and validation:

- ✅ GPT-4 story generation
- ✅ DALL-E image generation
- ✅ JSON response parsing
- ✅ Error handling
- ✅ Story continuity across scenes
- ✅ Response structure validation

**Example:**
```javascript
test('should generate valid story data structure', async () => {
  const mockClient = createMockOpenAI();
  const response = await mockClient.chat.completions.create({...});
  const storyData = JSON.parse(response.choices[0].message.content);

  expect(storyData).toHaveProperty('imagePrompt');
  expect(storyData).toHaveProperty('narrative');
  expect(storyData).toHaveProperty('nextSuggestion');
});
```

### 2. API Endpoint Tests (`api.test.js`)

Tests for Express API routes:

- ✅ GET /api/health endpoint
- ✅ POST /api/generate-scene endpoint
- ✅ Input validation
- ✅ Response structure
- ✅ Error handling

**Note:** These tests are templates. You'll need to export `app` from `server.js` to enable API testing.

### 3. Mock Helpers

#### `mockData.js`
Provides sample data for tests:
- User prompts
- GPT responses
- DALL-E responses
- Story history
- Test scenarios

#### `mockOpenAI.js`
Provides mock OpenAI clients:
- `createMockOpenAI()` - Standard mock
- `createFlakeyMockOpenAI()` - Mock that fails after N calls
- `verifyGPTCall()` - Verify GPT was called correctly
- `verifyDALLECall()` - Verify DALL-E was called correctly

**Example:**
```javascript
const mockClient = createMockOpenAI({
  gptShouldFail: false,
  dalleShouldFail: false,
  customGPTResponse: { your: 'response' }
});
```

## Documentation Files

### TEST_GUIDE.md (11KB)
Complete testing reference with:
- How to run tests
- Test structure overview
- Writing AI behavior tests
- Test templates
- Best practices
- Common assertions
- Quick reference card

### TDD_WORKFLOW.md (9KB)
Step-by-step TDD guide with:
- Red-Green-Refactor cycle explanation
- Real-world examples
- Daily TDD workflow
- Best practices checklist
- Common TDD patterns
- Troubleshooting tips

### template.test.js (8KB)
Copy-paste ready templates for:
- Basic unit tests
- AI behavior tests
- Image generation tests
- Data validation tests
- Edge case tests
- Async tests
- Integration tests
- Parametrized tests

## Quick Start

### 1. Install Dependencies

```bash
npm install
```

This installs:
- jest (test runner)
- supertest (HTTP testing)
- @jest/globals (test utilities)

### 2. Run Example Tests

```bash
npm test
```

The AI behavior tests will run using mocks (no API keys needed).

### 3. Write Your First Test

```bash
# Copy the template
cp __tests__/template.test.js __tests__/my-feature.test.js

# Edit and add your tests
# Run in watch mode
npm run test:watch
```

### 4. Follow TDD Workflow

1. **RED**: Write a failing test
2. **GREEN**: Write code to pass the test
3. **REFACTOR**: Clean up the code

See `TDD_WORKFLOW.md` for detailed examples.

## Test Coverage

Generate coverage reports:

```bash
npm run test:coverage
```

This creates a `coverage/` directory with:
- HTML report (open `coverage/lcov-report/index.html`)
- Line coverage
- Branch coverage
- Function coverage

## Example Test Scenarios Included

### Scenario 1: First Scene
```javascript
{
  userPrompt: "A young warrior discovers a magical sword",
  storyHistory: []
}
```

### Scenario 2: Story Continuation
```javascript
{
  userPrompt: "The warrior learns to wield the sword",
  storyHistory: [/* previous scenes */]
}
```

### Scenario 3: Long History
```javascript
{
  userPrompt: "The final battle begins",
  storyHistory: [/* 5+ scenes */]
}
```

## Adding More Tests

### For AI Features

1. Open `TEST_GUIDE.md`
2. Find "Template for Adding New AI Behavior Tests"
3. Copy the template
4. Customize for your feature
5. Run `npm test`

### For API Endpoints

1. Open `api.test.js`
2. Find "TEMPLATE FOR ADDING NEW API TESTS"
3. Copy the template
4. Customize for your endpoint
5. Run `npm test`

### Using Template File

```bash
# Copy template
cp __tests__/template.test.js __tests__/character-consistency.test.js

# Edit the new file
# Replace placeholders with your test logic

# Run your tests
npm run test:watch
```

## Next Steps

1. **Read the guides:**
   - Start with `TDD_WORKFLOW.md` for workflow
   - Reference `TEST_GUIDE.md` when writing tests

2. **Explore the tests:**
   - Look at `ai-behavior.test.js` for examples
   - Check `helpers/mockData.js` for test data patterns

3. **Add your own tests:**
   - Use `template.test.js` as a starting point
   - Test new features before implementing them

4. **Run tests regularly:**
   ```bash
   npm run test:watch  # Leave this running while coding
   ```

5. **Check coverage:**
   ```bash
   npm run test:coverage  # Aim for 80%+ coverage
   ```

## Common Tasks

### Test a New AI Feature

```javascript
// 1. Create test file
// __tests__/my-feature.test.js

const { createMockOpenAI } = require('./helpers/mockOpenAI');

describe('My New Feature', () => {
  test('should work as expected', async () => {
    const mock = createMockOpenAI();
    // Your test here
  });
});
```

### Add Test Data

```javascript
// Edit: __tests__/helpers/mockData.js

const myTestData = {
  input: "test input",
  expected: "expected output"
};

module.exports = {
  myTestData,
  // ... other exports
};
```

### Mock Custom Responses

```javascript
const customMock = createMockOpenAI({
  customGPTResponse: {
    imagePrompt: "Your custom prompt",
    narrative: "Your custom narrative",
    nextSuggestion: "Your custom suggestion"
  }
});
```

### Test Error Cases

```javascript
const failingMock = createMockOpenAI({
  gptShouldFail: true  // or dalleShouldFail: true
});

await expect(
  failingMock.chat.completions.create({...})
).rejects.toThrow();
```

## Tips for Success

1. **Write tests first** (before implementation)
2. **Keep tests focused** (one behavior per test)
3. **Use descriptive names** (explain what's being tested)
4. **Run tests frequently** (use watch mode)
5. **Aim for high coverage** (80%+ is good)
6. **Mock external APIs** (don't make real API calls in tests)
7. **Test edge cases** (empty, null, very long inputs)
8. **Refactor with confidence** (tests will catch breaks)

## Getting Help

- **Stuck on TDD?** Read `TDD_WORKFLOW.md`
- **Need test examples?** Check `ai-behavior.test.js`
- **Want templates?** Use `template.test.js`
- **Need reference?** See `TEST_GUIDE.md`
- **Jest docs:** https://jestjs.io/docs/getting-started

## Summary

You now have a complete TDD setup with:

✅ Jest test framework configured
✅ Mock OpenAI client for testing
✅ Sample test data and scenarios
✅ Example AI behavior tests
✅ Example API endpoint tests
✅ Comprehensive test templates
✅ Detailed TDD workflow guide
✅ Complete testing documentation

**Start testing with:** `npm run test:watch`

Happy Testing! 🧪
