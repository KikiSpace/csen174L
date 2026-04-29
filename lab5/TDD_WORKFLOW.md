# TDD Workflow Guide

This guide shows you how to follow Test-Driven Development (TDD) for the Anime Story Generator project.

## TDD Cycle: Red-Green-Refactor

```
┌─────────────┐
│   1. RED    │  Write a failing test
│   (Test)    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  2. GREEN   │  Write minimal code to pass
│   (Code)    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 3. REFACTOR │  Clean up and optimize
│  (Improve)  │
└──────┬──────┘
       │
       └──────────┐
                  │
       (Repeat)   │
                  ▼
```

## Example: Adding Character Consistency Feature

### Step 1: RED - Write the Test First

Create a new test file: `__tests__/character-consistency.test.js`

```javascript
const { describe, test, expect } = require('@jest/globals');
const { createMockOpenAI } = require('./helpers/mockOpenAI');

describe('Character Consistency', () => {
  test('should maintain character name across scenes', async () => {
    const mockClient = createMockOpenAI();

    // First scene mentions character name
    const scene1Response = await mockClient.chat.completions.create({
      model: 'gpt-4o',
      messages: [
        { role: 'user', content: 'A warrior named Kai discovers a sword' }
      ]
    });

    const scene1 = JSON.parse(scene1Response.choices[0].message.content);

    // We expect the function to extract character names
    const characters = extractCharacters(scene1.narrative);

    expect(characters).toContain('Kai');
  });
});
```

**Run the test:**
```bash
npm test
```

**Result:** ❌ Test fails (RED) because `extractCharacters` doesn't exist yet.

### Step 2: GREEN - Write Minimal Code

Create `utils/characterExtractor.js`:

```javascript
function extractCharacters(narrative) {
  // Simple implementation to make test pass
  const matches = narrative.match(/[A-Z][a-z]+/g);
  return matches || [];
}

module.exports = { extractCharacters };
```

Update your test to import it:
```javascript
const { extractCharacters } = require('../utils/characterExtractor');
```

**Run the test:**
```bash
npm test
```

**Result:** ✅ Test passes (GREEN)

### Step 3: REFACTOR - Improve the Code

Now improve the implementation:

```javascript
function extractCharacters(narrative) {
  // Better implementation with name detection
  const properNouns = narrative.match(/\b[A-Z][a-z]+\b/g) || [];

  // Filter out common words that aren't names
  const commonWords = ['The', 'A', 'An', 'In', 'As'];
  const names = properNouns.filter(word => !commonWords.includes(word));

  // Remove duplicates
  return [...new Set(names)];
}
```

**Run the test:**
```bash
npm test
```

**Result:** ✅ Test still passes, but code is better!

### Step 4: Add More Tests

Now that basic functionality works, add edge case tests:

```javascript
test('should handle multiple characters', () => {
  const narrative = "Kai and Yuki fought together";
  const characters = extractCharacters(narrative);

  expect(characters).toContain('Kai');
  expect(characters).toContain('Yuki');
});

test('should handle narratives with no characters', () => {
  const narrative = "the sword glowed brightly";
  const characters = extractCharacters(narrative);

  expect(characters).toHaveLength(0);
});
```

## TDD Workflow for New Features

### Adding "Story Genre Detection" Feature

#### 1. Write Test First (RED)

```javascript
// __tests__/genre-detection.test.js
describe('Genre Detection', () => {
  test('should detect fantasy genre from keywords', () => {
    const narrative = "A wizard cast a spell with his magic wand";
    const genre = detectGenre(narrative);

    expect(genre).toBe('fantasy');
  });

  test('should detect sci-fi genre', () => {
    const narrative = "The spaceship landed on the alien planet";
    const genre = detectGenre(narrative);

    expect(genre).toBe('sci-fi');
  });
});
```

Run test → ❌ Fails (no `detectGenre` function)

#### 2. Implement Function (GREEN)

```javascript
// utils/genreDetector.js
function detectGenre(narrative) {
  const fantasyKeywords = ['wizard', 'magic', 'spell', 'dragon', 'sword'];
  const scifiKeywords = ['spaceship', 'alien', 'robot', 'laser', 'planet'];

  const lowerText = narrative.toLowerCase();

  const hasFantasy = fantasyKeywords.some(word => lowerText.includes(word));
  const hasSciFi = scifiKeywords.some(word => lowerText.includes(word));

  if (hasFantasy) return 'fantasy';
  if (hasSciFi) return 'sci-fi';
  return 'general';
}

module.exports = { detectGenre };
```

Run test → ✅ Passes

#### 3. Refactor (IMPROVE)

```javascript
// Better implementation with more genres and scoring
function detectGenre(narrative) {
  const genres = {
    fantasy: ['wizard', 'magic', 'spell', 'dragon', 'sword', 'elf'],
    'sci-fi': ['spaceship', 'alien', 'robot', 'laser', 'planet', 'cyborg'],
    romance: ['love', 'heart', 'kiss', 'romance', 'dating'],
    action: ['fight', 'battle', 'explosion', 'chase', 'combat']
  };

  const lowerText = narrative.toLowerCase();
  const scores = {};

  for (const [genre, keywords] of Object.entries(genres)) {
    scores[genre] = keywords.filter(word => lowerText.includes(word)).length;
  }

  const topGenre = Object.entries(scores)
    .sort(([, a], [, b]) => b - a)[0];

  return topGenre[1] > 0 ? topGenre[0] : 'general';
}
```

Run test → ✅ Still passes, but more robust

## Daily TDD Workflow

### Morning Session

```bash
# 1. Start test watcher
npm run test:watch

# 2. Create new feature branch
git checkout -b feature/story-themes

# 3. Write first test
# Edit: __tests__/story-themes.test.js

# 4. Watch test fail automatically (RED)

# 5. Write code to pass test (GREEN)

# 6. Refactor code (IMPROVE)

# 7. Commit when all tests pass
git add .
git commit -m "Add story theme detection"
```

### Adding to Existing Feature

```bash
# 1. Run existing tests to ensure they pass
npm test

# 2. Write new test for additional behavior
# Edit: __tests__/ai-behavior.test.js

# 3. Watch it fail (RED)

# 4. Implement the feature (GREEN)

# 5. Refactor (IMPROVE)

# 6. Run full test suite
npm test

# 7. Check coverage
npm run test:coverage
```

## TDD Best Practices

### ✅ DO

1. **Write tests before code**
   ```javascript
   // First: Write test
   test('should format date', () => {
     expect(formatDate('2024-01-01')).toBe('Jan 1, 2024');
   });

   // Then: Implement function
   ```

2. **Keep tests simple and focused**
   ```javascript
   test('should validate email', () => {
     expect(isValidEmail('user@example.com')).toBe(true);
   });
   ```

3. **Test one behavior per test**
   ```javascript
   test('should extract first name', () => {
     expect(getFirstName('John Doe')).toBe('John');
   });

   test('should extract last name', () => {
     expect(getLastName('John Doe')).toBe('Doe');
   });
   ```

4. **Use descriptive test names**
   ```javascript
   test('should return empty array when narrative has no characters', () => {
     // ...
   });
   ```

### ❌ DON'T

1. **Write code before tests**
   ```javascript
   // Don't do this in TDD!
   function myFeature() { /* implemented first */ }
   test('should work', () => { /* test written after */ });
   ```

2. **Test implementation details**
   ```javascript
   // Bad: Testing internal variable
   test('should set internal counter', () => {
     expect(obj._counter).toBe(1);
   });

   // Good: Testing behavior
   test('should increment on each call', () => {
     obj.increment();
     expect(obj.getCount()).toBe(1);
   });
   ```

3. **Skip the refactor step**
   ```javascript
   // Don't leave messy code after test passes
   // Always refactor to clean, maintainable code
   ```

## TDD Checklist

Before committing code, verify:

- [ ] All tests pass (`npm test`)
- [ ] New feature has tests
- [ ] Tests follow Red-Green-Refactor cycle
- [ ] Code coverage is maintained (`npm run test:coverage`)
- [ ] Tests are readable and well-named
- [ ] No commented-out test code
- [ ] Edge cases are tested

## Common TDD Patterns

### Pattern 1: Test Data Transformation

```javascript
describe('Data Transformation', () => {
  test('should transform user input to prompt', () => {
    const input = "warrior finds sword";
    const prompt = transformToPrompt(input);

    expect(prompt).toContain('anime style');
    expect(prompt).toContain('warrior');
    expect(prompt).toContain('sword');
  });
});
```

### Pattern 2: Test Error Conditions

```javascript
describe('Error Handling', () => {
  test('should throw error for invalid input', () => {
    expect(() => processInput(null)).toThrow('Invalid input');
  });

  test('should return default for empty input', () => {
    expect(processInput('')).toBe(DEFAULT_VALUE);
  });
});
```

### Pattern 3: Test State Changes

```javascript
describe('State Management', () => {
  test('should update story history', () => {
    const history = new StoryHistory();
    history.addScene({ prompt: 'test' });

    expect(history.getSceneCount()).toBe(1);
  });
});
```

## Resources

- **Test Guide**: See `TEST_GUIDE.md` for detailed testing instructions
- **Test Template**: Copy `__tests__/template.test.js` for new test files
- **Mock Helpers**: Use helpers in `__tests__/helpers/` for consistent mocking

## Getting Help

If you're stuck:

1. Check existing tests for examples
2. Read `TEST_GUIDE.md` for common patterns
3. Run `npm test -- --help` for Jest options
4. Use `test.only()` to run single test while debugging

```javascript
test.only('should debug this specific test', () => {
  // Only this test will run
});
```
