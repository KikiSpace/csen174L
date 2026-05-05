# Deployment Guide: GitHub Pages + Backend

This guide explains how to deploy your Anime Story Generator with the frontend on GitHub Pages and the backend on a cloud service.

## Architecture

```
┌─────────────────────┐        API Requests         ┌──────────────────────┐
│   GitHub Pages      │   ─────────────────────>    │   Backend Server     │
│   (Frontend Only)   │                              │   (Node.js + OpenAI) │
│                     │   <─────────────────────    │                      │
└─────────────────────┘        JSON Responses       └──────────────────────┘
  kikispace.github.io                                  your-app.onrender.com
```

## Table of Contents

1. [Deploy Backend to Render (Free)](#step-1-deploy-backend-to-render)
2. [Configure Frontend for Production](#step-2-configure-frontend)
3. [Enable GitHub Pages](#step-3-enable-github-pages)
4. [Test Your Deployment](#step-4-test-deployment)
5. [Alternative Backend Hosts](#alternative-backend-hosts)
6. [Troubleshooting](#troubleshooting)

---

## Step 1: Deploy Backend to Render (Free)

Render offers free hosting for Node.js apps (perfect for this project).

### 1.1 Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Authorize Render to access your repositories

### 1.2 Create New Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your `csen174L` repository
3. Configure the service:

   ```
   Name: anime-story-generator (or any name you like)
   Region: Oregon (US West) or closest to you
   Branch: main
   Root Directory: lab5
   Runtime: Node
   Build Command: npm install
   Start Command: npm start
   Instance Type: Free
   ```

### 1.3 Add Environment Variables

In the Render dashboard:

1. Scroll to **"Environment Variables"**
2. Add:
   ```
   OPENAI_API_KEY = your_openai_api_key_here
   PORT = 10000
   ```
3. Click **"Save"**

### 1.4 Deploy

1. Click **"Create Web Service"**
2. Wait 2-5 minutes for deployment
3. Your backend will be at: `https://anime-story-generator.onrender.com`
4. **Copy this URL** - you'll need it next!

### 1.5 Test Backend

Visit: `https://your-app-name.onrender.com/api/health`

You should see:
```json
{
  "status": "ok",
  "message": "Server is running",
  "timestamp": "..."
}
```

---

## Step 2: Configure Frontend for Production

### 2.1 Update API URL

Edit `lab5/public/config.js`:

```javascript
const CONFIG = {
  API_URL: 'http://localhost:3000',

  // Change this to your Render URL!
  PRODUCTION_API_URL: 'https://anime-story-generator.onrender.com', // ← Your Render URL

  getApiUrl() {
    if (window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') {
      return this.PRODUCTION_API_URL;
    }
    return this.API_URL;
  }
};
```

### 2.2 Commit Changes

```bash
cd /Users/xinqizhang/Documents/CSEN174/lab5
git add public/config.js
git commit -m "Configure production API URL for Render backend"
git push origin main
```

---

## Step 3: Enable GitHub Pages

### 3.1 Enable Pages in Repository Settings

1. Go to your GitHub repository: https://github.com/KikiSpace/csen174L
2. Click **Settings** (top right)
3. Scroll to **Pages** (left sidebar)
4. Under **Source**, select:
   - Source: **GitHub Actions**
5. Click **Save**

### 3.2 Trigger Deployment

The GitHub Pages workflow will run automatically when you push. To trigger it manually:

1. Go to **Actions** tab
2. Click **"Deploy to GitHub Pages"**
3. Click **"Run workflow"** → **"Run workflow"**

### 3.3 Wait for Deployment

- Check the **Actions** tab for deployment status
- Takes 1-2 minutes
- Look for green checkmark ✅

### 3.4 Get Your GitHub Pages URL

Your app will be live at:

```
https://kikispace.github.io/csen174L/
```

**Note**: If you have a custom domain, update `server.js` CORS settings accordingly.

---

## Step 4: Test Deployment

### 4.1 Open Your App

Visit: https://kikispace.github.io/csen174L/

### 4.2 Check Console

1. Open browser DevTools (F12)
2. Go to Console tab
3. You should see:
   ```
   🌐 API Configuration: {
     hostname: "kikispace.github.io",
     apiUrl: "https://anime-story-generator.onrender.com",
     environment: "production"
   }
   Server status: { status: "ok", ... }
   ```

### 4.3 Test Story Generation

1. Enter a scene description
2. Click **"Generate Scene"**
3. Wait for image and narrative
4. Check that it works!

---

## Alternative Backend Hosts

### Option 1: Railway (Free $5 credit/month)

1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. **New Project** → **Deploy from GitHub repo**
4. Select `csen174L` → Configure:
   ```
   Root Directory: /lab5
   Start Command: npm start
   ```
5. Add Environment Variables:
   ```
   OPENAI_API_KEY=your_key
   PORT=3000
   ```
6. Get your URL: `https://your-app.up.railway.app`

### Option 2: Vercel (Free)

**Note**: Vercel works best for serverless functions. For Express apps, Render or Railway is recommended.

1. Go to [vercel.com](https://vercel.com)
2. Import your repository
3. Configure:
   ```
   Framework Preset: Other
   Root Directory: lab5
   Build Command: npm install
   Output Directory: public
   ```
4. Add Environment Variables
5. Deploy

### Option 3: Heroku (Paid - $5/month minimum)

Heroku no longer offers a free tier, but if you want to use it:

```bash
cd lab5
heroku create your-app-name
heroku config:set OPENAI_API_KEY=your_key
git subtree push --prefix lab5 heroku main
```

---

## Cost Breakdown

### Free Tier Hosting

| Service | Free Tier | Limitations |
|---------|-----------|-------------|
| GitHub Pages | Free forever | Static files only, 1GB storage |
| Render | 750 hours/month | Spins down after 15min inactivity |
| Railway | $5 credit/month | ~500 hours |
| Vercel | Free forever | 100GB bandwidth/month |

### API Costs (OpenAI)

- **DALL-E 3**: ~$0.040 per image
- **GPT-4o**: ~$0.005 per request
- **Per scene**: ~$0.045

**Monthly estimate** (100 scenes): ~$4.50

---

## Troubleshooting

### Frontend Not Connecting to Backend

**Symptom**: Alert saying "Cannot connect to server"

**Solutions**:

1. Check `config.js` has correct Render URL
2. Verify backend is running: visit `https://your-app.onrender.com/api/health`
3. Check browser console for CORS errors
4. Verify CORS is configured in `server.js`

### CORS Errors

**Error**: `Access to fetch at 'https://...' from origin 'https://kikispace.github.io' has been blocked by CORS`

**Solution**:

Edit `server.js` line 24:

```javascript
const allowedOrigins = [
  'http://localhost:3000',
  'http://127.0.0.1:3000',
  'https://kikispace.github.io', // ← Make sure this matches your GitHub Pages URL
  /\.github\.io$/
];
```

### Render App Sleeping

**Symptom**: First request takes 30+ seconds

**Cause**: Render free tier spins down after 15 minutes of inactivity

**Solutions**:

1. **Accept the delay**: Free tier limitation
2. **Keep alive service**: Use [cron-job.org](https://cron-job.org) to ping your app every 10 minutes
3. **Upgrade**: Render paid plan ($7/month) never sleeps

### GitHub Pages 404

**Symptom**: `https://kikispace.github.io/csen174L/` shows 404

**Solutions**:

1. Check GitHub Pages is enabled: Settings → Pages
2. Verify deployment succeeded: Actions tab → look for ✅
3. Wait 2-3 minutes after deployment
4. Hard refresh browser: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)

### Images Not Loading

**Symptom**: Narrative appears but image is broken

**Check**:

1. Backend logs in Render dashboard
2. OpenAI API key is correct
3. OpenAI account has credits
4. Browser console for errors

---

## Updating Your App

### Update Frontend Only

```bash
cd /Users/xinqizhang/Documents/CSEN174/lab5
# Make changes to public/index.html, public/app.js, etc.
git add public/
git commit -m "Update frontend UI"
git push origin main
# GitHub Pages redeploys automatically
```

### Update Backend Only

```bash
# Make changes to server.js
git add server.js
git commit -m "Update API logic"
git push origin main
# Render redeploys automatically
```

---

## Security Best Practices

### ✅ DO

- Keep `OPENAI_API_KEY` in environment variables (never commit to Git)
- Use HTTPS for production
- Configure CORS to only allow your domain
- Monitor API usage in OpenAI dashboard
- Set up rate limiting (future enhancement)

### ❌ DON'T

- Commit `.env` file (already in `.gitignore`)
- Share your API keys publicly
- Allow unlimited API requests (add rate limiting)
- Expose sensitive data in frontend

---

## Monitoring

### Check Backend Status

Visit: `https://your-app.onrender.com/api/health`

### Monitor API Costs

OpenAI Dashboard: https://platform.openai.com/usage

### Check GitHub Pages Status

Status page: https://www.githubstatus.com/

---

## Next Steps

1. ✅ Deploy backend to Render
2. ✅ Configure `config.js` with production URL
3. ✅ Enable GitHub Pages
4. ✅ Test your app
5. 🎉 Share your app with friends!

## Support

- **GitHub Issues**: [Create an issue](https://github.com/KikiSpace/csen174L/issues)
- **Render Docs**: https://render.com/docs
- **OpenAI API Docs**: https://platform.openai.com/docs

---

**Your app will be live at**:
- Frontend: https://kikispace.github.io/csen174L/
- Backend: https://your-app-name.onrender.com

Enjoy your deployed Anime Story Generator! 🎌📺
