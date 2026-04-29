# Test-Driven Development (TDD) Guide

This guide will help you write effective tests for the Anime Story Generator project.

## Table of Contents
1. [Running Tests](#running-tests)
2. [Test Structure](#test-structure)
3. [Writing AI Behavior Tests](#writing-ai-behavior-tests)
4. [Test Templates](#test-templates)
5. [Best Practices](#best-practices)

## Running Tests

```bash
# Run all tests once
npm test

# Run tests in watch mode (reruns on file changes)
npm run test:watch

# Run tests with coverage report
npm run test:coverage
```

## Test Structure

```
__tests__/
├── helpers/
│   ├── mockData.js       # Sample data for tests
│   └── mockOpenAI.js     # Mock OpenAI API client
├── api.test.js           # API endpoint tests
└── ai-behavior.test.js   # AI response tests
```

## Writing AI Behavior Tests

### 1. Basic AI Response Test

```javascript
const { createMockOpenAI } = require('./helpers/mockOpenAI');

test('should generate valid AI response', async () => {
  // Setup: Create mock client
  const mockClient = createMockOpenAI();

  // Execute: Call AI function
  const response = await mockClient.chat.completions.create({
    model: 'gpt-4o',
    messages: [
      { role: 'system', content: 'You are a helpful assistant.' },
      { role: 'user', content: 'Generate a story' }
    ]
  });

  // Assert: Verify response
  const data = JSON.parse(response.choices[0].message.content);
  expect(data).toHaveProperty('imagePrompt');
  expect(data).toHaveProperty('narrative');
  expect(data).toHaveProperty('nextSuggestion');
});
```

### 2. Testing with Custom Responses

```javascript
test('should handle custom AI response', async () => {
  const customResponse = {
    imagePrompt: "Custom anime scene",
    narrative: "Custom story",
    nextSuggestion: "What happens next"
  };

  const mockClient = createMockOpenAI({
    customGPTResponse: customResponse
  });

  const response = await mockClient.chat.completions.create({
    model: 'gpt-4o',
    messages: [{ role: 'user', content: 'test' }]
  });

  const data = JSON.parse(response.choices[0].message.content);
  expect(data).toEqual(customResponse);
});
```

### 3. Testing Error Scenarios

```javascript
test('should handle AI API errors', async () => {
  const failingMock = createMockOpenAI({ gptShouldFail: true });

  await expect(
    failingMock.chat.completions.create({
      model: 'gpt-4o',
      messages: [{ role: 'user', content: 'test' }]
    })
  ).rejects.toThrow();
});
```

### 4. Testing Data Validation

```javascript
test('should validate AI response format', async () => {
  const mockClient = createMockOpenAI();

  const response = await mockClient.chat.completions.create({
    model: 'gpt-4o',
    messages: [{ role: 'user', content: 'Generate story' }]
  });

  const data = JSON.parse(response.choices[0].message.content);

  // Validate field types
  expect(typeof data.imagePrompt).toBe('string');
  expect(typeof data.narrative).toBe('string');
  expect(typeof data.nextSuggestion).toBe('string');

  // Validate field lengths
  expect(data.imagePrompt.length).toBeGreaterThan(10);
  expect(data.narrative.length).toBeGreaterThan(10);
});
```

## Test Templates

### Template 1: Testing New AI Feature

```javascript
describe('Your New AI Feature', () => {
  let mockOpenAI;

  beforeEach(() => {
    mockOpenAI = createMockOpenAI();
  });

  test('should generate expected output', async () => {
    // 1. Setup test data
    const input = 'your test input';

    // 2. Call AI function
    const response = await mockOpenAI.chat.completions.create({
      model: 'gpt-4o',
      messages: [{ role: 'user', content: input }]
    });

    // 3. Parse response
    const result = JSON.parse(response.choices[0].message.content);

    // 4. Verify output
    expect(result).toHaveProperty('expectedField');
    expect(result.expectedField).toBeTruthy();
  });

  test('should handle edge cases', async () => {
    // Test with empty string, very long string, special characters, etc.
  });

  test('should maintain consistency', async () => {
    // Test that multiple calls with same input produce valid outputs
  });
});
```

### Template 2: Testing Story Continuity

```javascript
describe('Story Continuity', () => {
  test('should maintain context across scenes', async () => {
    const mockClient = createMockOpenAI();
    const storyHistory = [];

    // Generate Scene 1
    const scene1Response = await mockClient.chat.completions.create({
      model: 'gpt-4o',
      messages: [
        { role: 'user', content: 'Scene 1 description' }
      ]
    });

    const scene1 = JSON.parse(scene1Response.choices[0].message.content);
    storyHistory.push(scene1);

    // Generate Scene 2 with context
    const contextPrompt = buildContextPrompt(storyHistory);
    const scene2Response = await mockClient.chat.completions.create({
      model: 'gpt-4o',
      messages: [
        { role: 'user', content: contextPrompt }
      ]
    });

    const scene2 = JSON.parse(scene2Response.choices[0].message.content);

    // Verify continuity
    expect(scene2).toHaveProperty('narrative');
    expect(scene2.narrative).toBeTruthy();
  });
});

function buildContextPrompt(history) {
  return history.map((h, i) =>
    `Scene ${i + 1}: ${h.narrative}`
  ).join('\n\n');
}
```

### Template 3: Testing Response Parsing

```javascript
describe('Response Parsing', () => {
  test('should parse JSON correctly', () => {
    const mockResponse = {
      imagePrompt: "Test prompt",
      narrative: "Test narrative",
      nextSuggestion: "Test suggestion"
    };

    const jsonString = JSON.stringify(mockResponse);
    const parsed = JSON.parse(jsonString);

    expect(parsed).toEqual(mockResponse);
  });

  test('should extract JSON from markdown', () => {
    const responseWithMarkdown = \`
      Here's the data:
      \\\`\\\`\\\`json
      {"imagePrompt": "test"}
      \\\`\\\`\\\`
    \`;

    const jsonMatch = responseWithMarkdown.match(/\\{[\\s\\S]*\\}/);
    const parsed = JSON.parse(jsonMatch[0]);

    expect(parsed).toHaveProperty('imagePrompt');
  });

  test('should handle malformed JSON', () => {
    const malformedJSON = '{ "field": "value", }'; // Trailing comma

    expect(() => JSON.parse(malformedJSON)).toThrow();
  });
});
```

### Template 4: Integration Test

```javascript
describe('End-to-End Scene Generation', () => {
  test('should complete full generation workflow', async () => {
    const mockClient = createMockOpenAI();
    const userPrompt = "A warrior finds a sword";

    // Step 1: Generate story data with GPT
    const storyResponse = await mockClient.chat.completions.create({
      model: 'gpt-4o',
      messages: [
        { role: 'system', content: 'You are an anime story creator.' },
        { role: 'user', content: userPrompt }
      ]
    });

    const storyData = JSON.parse(storyResponse.choices[0].message.content);

    // Step 2: Generate image with DALL-E
    const imageResponse = await mockClient.images.generate({
      model: "dall-e-3",
      prompt: storyData.imagePrompt + " anime style",
      size: "1024x1024"
    });

    // Verify complete workflow
    expect(storyData).toHaveProperty('imagePrompt');
    expect(storyData).toHaveProperty('narrative');
    expect(storyData).toHaveProperty('nextSuggestion');
    expect(imageResponse.data[0]).toHaveProperty('url');
    expect(imageResponse.data[0].url).toMatch(/^https?:\\/\\//);
  });
});
```

## Best Practices

### 1. Arrange-Act-Assert Pattern

```javascript
test('should follow AAA pattern', async () => {
  // Arrange: Set up test data and mocks
  const mockClient = createMockOpenAI();
  const input = 'test input';

  // Act: Execute the function being tested
  const response = await mockClient.chat.completions.create({
    model: 'gpt-4o',
    messages: [{ role: 'user', content: input }]
  });

  // Assert: Verify the results
  expect(response).toBeTruthy();
});
```

### 2. Use Descriptive Test Names

```javascript
// ❌ Bad
test('test 1', () => { });

// ✅ Good
test('should generate anime-style image prompt with detailed description', () => { });
```

### 3. Test One Thing at a Time

```javascript
// ❌ Bad - testing multiple concerns
test('should do everything', () => {
  expect(response).toBeTruthy();
  expect(database).toBeSaved();
  expect(email).toBeSent();
});

// ✅ Good - focused tests
test('should generate valid response', () => {
  expect(response).toBeTruthy();
});

test('should save to database', () => {
  expect(database).toBeSaved();
});
```

### 4. Use beforeEach for Common Setup

```javascript
describe('AI Feature Tests', () => {
  let mockClient;
  let testData;

  beforeEach(() => {
    mockClient = createMockOpenAI();
    testData = { prompt: 'test' };
  });

  test('test 1', () => {
    // mockClient and testData are available
  });

  test('test 2', () => {
    // Fresh mockClient and testData for each test
  });
});
```

### 5. Test Edge Cases

```javascript
describe('Edge Cases', () => {
  test('should handle empty input', async () => {
    // Test with empty string
  });

  test('should handle very long input', async () => {
    const longInput = 'a'.repeat(10000);
    // Test with long string
  });

  test('should handle special characters', async () => {
    const specialInput = '!@#$%^&*(){}[]';
    // Test with special characters
  });

  test('should handle unicode characters', async () => {
    const unicodeInput = '日本語のテスト';
    // Test with unicode
  });
});
```

### 6. Mock External Dependencies

```javascript
// Always mock external APIs
jest.mock('openai', () => {
  return jest.fn().mockImplementation(() => {
    return createMockOpenAI();
  });
});
```

### 7. Write Tests First (TDD)

1. **Red**: Write a failing test
2. **Green**: Write minimal code to pass
3. **Refactor**: Clean up the code

```javascript
// Step 1: Write failing test
test('should generate character description', () => {
  const result = generateCharacterDescription('warrior');
  expect(result).toContain('warrior');
});

// Step 2: Implement function
function generateCharacterDescription(type) {
  return `A brave ${type} appears`;
}

// Step 3: Refactor if needed
```

## Common Assertions

```javascript
// Equality
expect(value).toBe(expected);
expect(value).toEqual(expected);

// Truthiness
expect(value).toBeTruthy();
expect(value).toBeFalsy();

// Numbers
expect(value).toBeGreaterThan(3);
expect(value).toBeLessThan(10);

// Strings
expect(string).toMatch(/pattern/);
expect(string).toContain('substring');

// Arrays
expect(array).toHaveLength(3);
expect(array).toContain(item);

// Objects
expect(object).toHaveProperty('key');
expect(object).toMatchObject({ key: 'value' });

// Exceptions
expect(() => fn()).toThrow();
expect(() => fn()).toThrow('error message');

// Async
await expect(promise).resolves.toBe(value);
await expect(promise).rejects.toThrow();
```

## Quick Reference Card

| Task | Code |
|------|------|
| Create mock client | `const mock = createMockOpenAI()` |
| Custom response | `createMockOpenAI({ customGPTResponse: data })` |
| Failing mock | `createMockOpenAI({ gptShouldFail: true })` |
| Verify GPT call | `verifyGPTCall(mock, { model: 'gpt-4o' })` |
| Verify DALL-E call | `verifyDALLECall(mock, { size: '1024x1024' })` |
| Use test data | `const { mockUserPrompts } = require('./helpers/mockData')` |

## Further Resources

- [Jest Documentation](https://jestjs.io/docs/getting-started)
- [Testing Best Practices](https://testingjavascript.com/)
- [TDD Guide](https://martinfowler.com/bliki/TestDrivenDevelopment.html)
