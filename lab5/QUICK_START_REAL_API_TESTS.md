# Quick Start: Real API Testing

## 🚀 Run Tests with Real OpenAI API

Follow these steps to test with the **actual OpenAI API** instead of mocks.

## Step 1: Check Your API Key

Make sure you have an OpenAI API key in your `.env` file:

```bash
# Check if .env exists
cat .env

# Should see:
OPENAI_API_KEY=sk-proj-your-actual-key-here
```

If you don't have a `.env` file:

```bash
# Copy example
cp .env.example .env

# Edit with your key
nano .env  # or use your editor
```

Get your API key from: https://platform.openai.com/api-keys

## Step 2: Install Dependencies

```bash
npm install
```

## Step 3: Run Integration Tests

```bash
npm run test:integration
```

## What You'll See

```
$ npm run test:integration

⚠️  Running REAL API tests - this will cost money!

Real API Integration Tests
  GPT-4 Real API
    📝 GPT-4 Response: {
      "imagePrompt": "A young warrior in classic 1980s anime style...",
      "narrative": "In the depths of the forgotten temple...",
      "nextSuggestion": "The temple begins to collapse..."
    }
    ✓ should generate valid story data with real GPT-4 (2431ms)

    🎨 Image Prompt: Vintage 1980s anime style warrior discovering...
    ✓ should include vintage anime style in prompts (1823ms)

    📖 Story Continuation: The warrior's connection to the sword...
    ✓ should generate coherent story continuation (2156ms)

  DALL-E 3 Real API
    🖼️  Generated Image URL: https://oaidalleapiprodscus.blob.core...
    📝 Revised Prompt: A young anime warrior with determined eyes...
    ✓ should generate real anime image with DALL-E 3 (12156ms)

  Full End-to-End Workflow
    🚀 Starting full workflow test...
    📝 Step 1: Generating story with GPT-4...
    ✅ Story generated: {
      imagePrompt: "A mecha pilot in vintage 1970s anime...",
      narrative: "The young pilot climbs into the cockpit...",
      nextSuggestion: "The mecha activates for the first time..."
    }
    🎨 Step 2: Generating image with DALL-E...
    ✅ Image generated: https://oaidalleapiprodscus.blob...
    ✅ Complete scene generated successfully!
    ✓ should complete full scene generation workflow (15234ms)

  Error Handling with Real API
    ✓ should handle invalid model name (234ms)
    ✓ should handle empty prompt (1567ms)

Tests: 7 passed, 7 total
Time: 32.145s

Cost: ~$0.10
```

## Understanding the Output

### 📝 Story Generation
- **Real GPT-4 response** with actual generated content
- Shows the `imagePrompt`, `narrative`, and `nextSuggestion`
- Validates vintage anime keywords are included

### 🎨 Image Generation
- **Real DALL-E 3 image** generated
- Shows actual image URL (valid for 1 hour)
- Shows DALL-E's revised prompt

### ⏱️ Timing
- GPT-4 tests: ~2-3 seconds each
- DALL-E tests: ~10-15 seconds each
- Full workflow: ~15-20 seconds

### 💰 Cost
- GPT-4o: ~$0.005 per test
- DALL-E 3: ~$0.04 per image
- **Total**: ~$0.10 per full test run

## Running Specific Tests

### Only GPT-4 Tests

```bash
npm run test:integration -- -t "GPT-4"
```

### Only DALL-E Tests

```bash
npm run test:integration -- -t "DALL-E"
```

### Only Full Workflow

```bash
npm run test:integration -- -t "Full End-to-End"
```

### Single Test

```bash
npm run test:integration -- -t "should generate valid story"
```

## Comparing Mock vs Real

Run both to see the difference:

```bash
# Mock tests (fast, free)
npm run test:unit

# Real API tests (slow, costs money)
npm run test:integration
```

## Common Issues

### Issue: Tests Skipped

```
⚠️  Integration tests skipped
To run these tests:
1. Set OPENAI_API_KEY in your .env file
2. Run: npm run test:integration
```

**Fix**: Add your API key to `.env`

### Issue: Rate Limit Error

```
Error: 429 Rate Limit Exceeded
```

**Fix**: Wait 60 seconds and retry

```bash
sleep 60 && npm run test:integration
```

### Issue: Timeout Error

```
Timeout - Async callback was not invoked within the 5000ms timeout
```

**Fix**: Already handled! Tests have extended timeouts:
- GPT-4: 30 seconds
- DALL-E: 60 seconds
- Full workflow: 90 seconds

### Issue: High Costs

**Fix**: Use unit tests for development, integration tests only before deployment

```bash
# Daily development - FREE
npm run test:unit

# Pre-deployment only - $0.10
npm run test:integration
```

## When to Use Each

### Use Unit Tests (Mock) - Daily

```bash
npm test
# or
npm run test:watch
```

**For:**
- 🔄 TDD development
- 🚀 Fast feedback
- 💰 No costs
- ✅ CI/CD pipelines

### Use Integration Tests (Real API) - Occasionally

```bash
npm run test:integration
```

**For:**
- 🎯 Pre-deployment validation
- 🔍 Debugging real API issues
- ✅ Verifying prompt changes work
- 🆕 Testing after OpenAI updates

## Best Practice Workflow

```bash
# 1. Development phase - use mocks
npm run test:watch

# 2. Before committing - verify unit tests pass
npm test

# 3. Before deployment - validate with real API
npm run test:integration

# 4. Deploy with confidence! ✅
```

## What Gets Tested

### ✅ GPT-4 Behavior
- Valid JSON response structure
- Vintage anime style keywords in prompts
- Coherent story continuations
- Error handling

### ✅ DALL-E 3 Behavior
- Image generation succeeds
- Returns valid image URLs
- Accepts vintage anime prompts

### ✅ Full Integration
- GPT-4 → DALL-E workflow
- Complete scene generation
- All data properly formatted

## Next Steps

1. ✅ Run the tests
2. 📸 Check the generated image URLs in the output
3. 📊 Compare results with mock tests
4. 🎨 Verify vintage anime style in generated images

## Pro Tips

### Save on Costs

```bash
# Run only when necessary
npm run test:integration

# Not on every code change!
```

### Debug Specific Issues

```bash
# Target specific functionality
npm run test:integration -- -t "GPT-4"
```

### Watch Real Responses

The tests log actual API responses, so you can see:
- What GPT-4 actually generates
- What prompts DALL-E receives
- What images get created

### Continuous Integration

Only run integration tests on main branch:

```yaml
# GitHub Actions
if: github.ref == 'refs/heads/main'
run: npm run test:integration
```

## Summary

| Command | When | Cost | Time |
|---------|------|------|------|
| `npm test` | Daily dev | Free | 1s |
| `npm run test:integration` | Pre-deploy | $0.10 | 30s |

**Recommendation**: Develop with mocks, validate with real API before deployment.

---

**Full Documentation**: [REAL_API_TESTING.md](REAL_API_TESTING.md)
