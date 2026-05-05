# Jest Test Markers Guide: Skip, Todo, and Failing Tests

This guide shows how to mark tests that aren't ready to run or are expected to fail.

## Quick Reference

| Marker | Purpose | Example |
|--------|---------|---------|
| `test.skip()` | Skip a test temporarily | `test.skip('test name - SKIP: reason', () => {...})` |
| `test.todo()` | Placeholder for future test | `test.todo('test name - TODO: reason')` |
| `test.failing()` | Test expected to fail | `test.failing('test name - XFAIL: reason', () => {...})` |

---

## 1. SKIP - Temporarily Disable a Test

Use `test.skip()` when you have a working test but don't want to run it right now.

### Basic Usage

```javascript
test.skip('should do something', () => {
  expect(true).toBe(false);
});
```

### With Reason in Test Name (Recommended)

```javascript
test.skip('should cache images - SKIP: Redis not configured in CI', () => {
  const cache = getRedisCache();
  expect(cache).toBeDefined();
});
```

### Skip Entire Test Suite

```javascript
describe.skip('Integration Tests - SKIP: API endpoint down', () => {
  test('should call API', () => {
    // All tests in this block are skipped
  });

  test('should handle errors', () => {
    // This is also skipped
  });
});
```

### When to Use SKIP

- ✅ Test is flaky and needs investigation
- ✅ Feature is temporarily disabled
- ✅ Test depends on external service that's unavailable
- ✅ Test is being refactored
- ❌ Test never worked (use `test.failing` instead)
- ❌ Test not written yet (use `test.todo` instead)

---

## 2. TODO - Placeholder for Future Tests

Use `test.todo()` to mark tests you plan to write but haven't implemented yet.

### Basic Usage

```javascript
test.todo('should export story as PDF');
```

### With Reason (Recommended)

```javascript
test.todo('should export story as PDF - TODO: Waiting for PDF library selection');
test.todo('should track character consistency - TODO: Character DB schema needed');
test.todo('should support multiple art styles - TODO: Blocked by ISSUE-123');
```

### Important Notes

- `test.todo()` only takes a **string**, no function body
- Shows in test output as "todo"
- Helps track technical debt
- Good for TDD: write test names first, implement later

### When to Use TODO

- ✅ Planning test coverage
- ✅ Following TDD (write test names before implementation)
- ✅ Tracking missing tests during code review
- ✅ Documenting future test requirements
- ❌ Test is partially written (commit it as `test.skip` instead)

---

## 3. FAILING - Expected to Fail (like pytest's xfail)

Use `test.failing()` when a test currently fails, but you expect it to pass in the future.

### Basic Usage

```javascript
test.failing('should handle edge case', () => {
  expect(buggyFunction()).toBe('correct');
  // This test fails now, but that's expected
});
```

### With Reason (Recommended)

```javascript
test.failing('should retry failed API calls - XFAIL: Retry logic not implemented', async () => {
  const result = await apiCallWithRetry();
  expect(result).toBeDefined();
});
```

### How It Works

| Test Result | What It Means | Jest Shows |
|-------------|---------------|------------|
| Test fails | "Good! Still failing as expected" | ✅ PASS |
| Test passes | "Unexpected! Test now works!" | ❌ FAIL |

When the bug is fixed, the test will start "failing" (because it passed), alerting you to remove `.failing`.

### When to Use FAILING

- ✅ Known bug with test already written
- ✅ Feature partially implemented
- ✅ Test for future behavior (TDD)
- ✅ Documenting expected behavior before fix
- ❌ Test will never pass (delete it or document why)
- ❌ Test is flaky (use `test.skip` and fix flakiness)

---

## 4. Naming Conventions

### Recommended Pattern

Include the marker and reason in the test name:

```javascript
test.skip('feature name - SKIP: reason why skipped', () => {...});
test.todo('feature name - TODO: reason for deferral');
test.failing('feature name - XFAIL: reason it fails', () => {...});
```

### Real Examples

```javascript
// SKIP Examples
test.skip('should upload to S3 - SKIP: AWS credentials not in CI environment', () => {...});
test.skip('should send email - SKIP: Email service being migrated', () => {...});
test.skip('performance test - SKIP: Flaky in CI, investigating', () => {...});

// TODO Examples
test.todo('should paginate results - TODO: Pagination API not designed yet');
test.todo('should validate input - TODO: Waiting for validation rules from PM');
test.todo('should log errors - TODO: Logger implementation pending');

// FAILING Examples
test.failing('should parse dates - XFAIL: Date library bug, waiting for v2.0', () => {...});
test.failing('should compress images - XFAIL: Compression ratio too low', () => {...});
test.failing('should handle 1M requests - XFAIL: Performance optimization needed', () => {...});
```

---

## 5. Conditional Skipping

Skip tests based on environment or conditions:

### Helper Functions

```javascript
const describeIf = (condition) => condition ? describe : describe.skip;
const testIf = (condition) => condition ? test : test.skip;
```

### Usage

```javascript
// Only run if API key is available
testIf(process.env.OPENAI_API_KEY)('should call OpenAI API', async () => {
  // Test implementation
});

// Only run in CI environment
testIf(process.env.CI)('should run integration tests', async () => {
  // Test implementation
});

// Skip in Windows
testIf(process.platform !== 'win32')('should use unix paths', () => {
  // Test implementation
});
```

---

## 6. Best Practices

### ✅ DO

- **Always include a reason**: Explain WHY the test is skipped/todo/failing
- **Link to issues**: Reference ticket numbers when applicable
- **Keep it temporary**: Regularly review and remove markers
- **Use in CI**: All three markers work in GitHub Actions
- **Document deadlines**: Add expected completion dates in comments

```javascript
test.skip('should cache results - SKIP: Blocked by ISSUE-456', () => {
  // Expected fix: Sprint 12
  // Assigned to: @developer
  // More info: https://github.com/org/repo/issues/456
});
```

### ❌ DON'T

- **Don't skip to hide failures**: Fix the test instead
- **Don't leave markers forever**: Clean up regularly
- **Don't use for performance**: Use `test.skip` wisely, don't slow CI
- **Don't nest unnecessarily**: Avoid `describe.skip` inside `describe.skip`

---

## 7. Viewing Skipped/Todo/Failing Tests

### Run All Tests

```bash
npm test
```

Output shows:
- ✅ PASS: Tests that passed (including expected failures)
- ❌ FAIL: Tests that failed unexpectedly
- ⊘ SKIP: Tests that were skipped
- ○ TODO: Tests marked as todo

### Show Only Skipped Tests

```bash
npm test -- --listTests
npm test -- --verbose
```

### Show Summary

```bash
npm test -- --verbose
```

Look for:
```
Test Suites: 1 passed, 1 total
Tests:       5 passed, 3 skipped, 2 todo, 1 failing, 11 total
```

---

## 8. Real-World Examples for Anime Story Generator

```javascript
describe('Anime Story Generator Tests', () => {

  // ========== TODO: Future Features ==========
  test.todo('should save story to database - TODO: Database schema design pending');
  test.todo('should export as PDF - TODO: PDF library evaluation (PDFKit vs jsPDF)');
  test.todo('should support character memory - TODO: Vector DB integration');
  test.todo('should allow branching narratives - TODO: Graph data structure needed');

  // ========== SKIP: Temporarily Disabled ==========
  test.skip('should compress images - SKIP: Image optimization library removed in v2.0', () => {
    // Feature removed, but keeping test for potential re-add
  });

  test.skip('should limit API costs - SKIP: Billing API not available in test env', () => {
    // Can't test billing logic without production API
  });

  test.skip('should generate video - SKIP: OpenAI video API not released yet', async () => {
    // Waiting for Sora API
  });

  // ========== FAILING: Known Issues ==========
  test.failing('should handle 50+ scene stories - XFAIL: Token limit bug, see BUG-789', async () => {
    // Known: Crashes after 50 scenes due to context window
    // Fix scheduled for v3.1
    const longStory = createStoryWithScenes(55);
    expect(() => processStory(longStory)).not.toThrow();
  });

  test.failing('should maintain art style consistency - XFAIL: DALL-E 3 style drift', async () => {
    // Known DALL-E limitation: style changes between generations
    // Exploring fine-tuning options
    const scenes = await generateScenes(5);
    expect(areSimilarStyle(scenes)).toBe(true);
  });

});
```

---

## 9. GitHub Actions Integration

All three markers work perfectly in CI:

### Workflow Behavior

- **SKIP**: Doesn't run, doesn't affect pass/fail
- **TODO**: Shown in output, doesn't affect pass/fail
- **FAILING**: Runs and passes if it fails (as expected)

### CI Output Example

```
PASS  __tests__/ai-behavior.test.js
  ✓ should generate story (245 ms)
  ○ skipped should cache images - SKIP: Redis not in CI
  ○ todo should export PDF - TODO: Library selection pending
  ✓ should handle errors (EXPECTED FAILURE) (156 ms)

Tests: 2 passed, 1 skipped, 1 todo, 1 failing, 5 total
```

---

## 10. Migration from Other Frameworks

### From Pytest

| Pytest | Jest |
|--------|------|
| `@pytest.mark.skip(reason="...")` | `test.skip('... - SKIP: reason', ...)` |
| `@pytest.mark.xfail(reason="...")` | `test.failing('... - XFAIL: reason', ...)` |
| N/A | `test.todo('... - TODO: reason')` |

### From Mocha

| Mocha | Jest |
|-------|------|
| `it.skip('test')` | `test.skip('test - SKIP: reason')` |
| `xit('test')` | `test.skip('test - SKIP: reason')` |
| N/A (use `it.skip`) | `test.todo('test - TODO: reason')` |
| N/A | `test.failing('test - XFAIL: reason')` |

---

## Need Help?

- **Jest Docs**: https://jestjs.io/docs/api#testskipname-fn
- **Examples**: See `__tests__/examples/test-markers.example.js`
- **CI Integration**: See `.github/workflows/README.md`

---

**Remember**: These markers are tools for managing technical debt. Use them wisely, document reasons clearly, and clean them up regularly!
