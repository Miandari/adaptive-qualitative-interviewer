# Streamlit Cloud Deployment Guide

## Quick Start Checklist

✅ **Prerequisites (Already Done):**
- [x] Dependencies pinned in `requirements.txt`
- [x] `.streamlit/config.toml` created
- [x] `.streamlit/secrets.toml.example` template
- [x] `.gitignore` updated to exclude secrets
- [x] Repository pushed to GitHub

## Deployment Steps

### 1. Sign Up for Streamlit Cloud

1. Go to https://streamlit.io/cloud
2. Click "Sign up" or "Sign in"
3. Connect with your GitHub account
4. Authorize Streamlit to access your repositories

### 2. Deploy Your App

1. Click **"New app"** button
2. Fill in the deployment form:
   - **Repository:** Select `Miandari/adaptive-qualitative-interviewer`
   - **Branch:** `main`
   - **Main file path:** `interfaces/streamlit_app.py`
   - **App URL:** Choose your subdomain (e.g., `adaptive-interviewer`)

3. Click **"Deploy!"**

### 3. Configure Secrets (IMPORTANT!)

Once deployed, you need to add your API keys:

1. Go to your app dashboard
2. Click **"⚙️ Settings"**
3. Click **"Secrets"** in the sidebar
4. Paste your secrets in TOML format:

**For OpenAI:**
```toml
OPENAI_API_KEY = "sk-your-actual-openai-key-here"
LLM_PROVIDER = "openai"
LLM_MODEL = "gpt-4o"
TEMPERATURE = 0.7
```

**For Anthropic:**
```toml
ANTHROPIC_API_KEY = "sk-ant-your-actual-anthropic-key-here"
LLM_PROVIDER = "anthropic"
LLM_MODEL = "claude-3-5-sonnet-20241022"
TEMPERATURE = 0.7
```

5. Click **"Save"**
6. Your app will automatically restart with the new secrets

### 4. Test Your Deployment

1. Wait for deployment to complete (usually 2-3 minutes)
2. Visit your app URL: `https://your-app-name.streamlit.app`
3. Select an experiment
4. Fill in participant info
5. Test a conversation

### 5. Share Your App

Your app is now live! Share the URL with:
- Research participants
- Collaborators
- Study coordinators

## Managing Your Deployment

### Auto-Updates

Every time you push to GitHub, Streamlit Cloud automatically:
- Pulls the latest code
- Reinstalls dependencies
- Restarts the app

**To deploy updates:**
```bash
git add .
git commit -m "Your update message"
git push origin main
```

App updates automatically in ~2 minutes!

### Viewing Logs

1. Go to your app dashboard
2. Click **"Manage app"**
3. Click **"Logs"** tab
4. View real-time logs and errors

### Managing Resources

**Free Tier Includes:**
- ✅ Unlimited public apps
- ✅ 1 GB RAM per app
- ✅ Auto-sleep after inactivity (wakes on visit)
- ✅ Community support

**If you need more:**
- Upgrade to paid tier for:
  - More resources
  - Private apps
  - Custom domains
  - Priority support

## Troubleshooting

### App Won't Start

**Check logs for errors:**
1. Missing dependencies → Update `requirements.txt`
2. Import errors → Check `PYTHONPATH` in code
3. Secrets not configured → Add secrets in settings

### API Key Errors

**Symptoms:** "Authentication failed" or "Invalid API key"

**Solution:**
1. Go to app settings → Secrets
2. Verify API key format
3. Ensure no extra spaces or quotes in the key
4. Make sure `LLM_PROVIDER` matches the key you're using

### Slow Performance

**Symptoms:** App takes long to respond

**Possible causes:**
- Model choice (gpt-4o is slower than gpt-3.5-turbo)
- Cold start after sleep
- High traffic

**Solutions:**
- Use faster model for testing
- Upgrade to paid tier for always-on apps
- Optimize conversation prompts

### Module Not Found

**Symptoms:** `ModuleNotFoundError: No module named 'X'`

**Solution:**
1. Add missing package to `requirements.txt`
2. Push to GitHub
3. App will auto-update

## Security Best Practices

### ✅ Do:
- Use Streamlit Cloud secrets for API keys
- Keep `.streamlit/secrets.toml` in `.gitignore`
- Rotate API keys periodically
- Monitor usage to detect unauthorized access

### ❌ Don't:
- Commit API keys to GitHub
- Share secrets in public channels
- Use production keys for testing
- Leave secrets in code comments

## Cost Considerations

### Streamlit Cloud (Free Tier)
- **Cost:** $0
- **Limits:** Public apps, 1 GB RAM, community support
- **Good for:** Research studies, pilots, small scale

### LLM API Costs
Track your usage:
- **OpenAI:** https://platform.openai.com/usage
- **Anthropic:** https://console.anthropic.com/usage

**Typical costs per conversation:**
- GPT-4o: ~$0.05-0.15 per 5-8 exchanges
- Claude 3.5 Sonnet: ~$0.10-0.20 per 5-8 exchanges

**For 100 participants:**
- Expect: $5-20 total depending on model and depth

## Advanced Configuration

### Custom Domain (Paid Tier)

1. Upgrade to paid tier
2. Go to app settings
3. Add custom domain
4. Update DNS records

### Analytics

Track usage with:
- Streamlit Cloud analytics (basic)
- Google Analytics (add to app)
- Custom logging in code

### Backup Data

Export session data regularly:
- Use export functionality in app
- Or access via FastAPI endpoints
- Store in secure location

## Support

### Streamlit Community
- Forum: https://discuss.streamlit.io
- Docs: https://docs.streamlit.io
- GitHub: https://github.com/streamlit/streamlit

### Project Issues
- GitHub Issues: https://github.com/Miandari/adaptive-qualitative-interviewer/issues

## Next Steps

After deployment:

1. ✅ Test all experiments
2. ✅ Verify data export works
3. ✅ Share URL with pilot participants
4. ✅ Monitor logs for errors
5. ✅ Track API usage/costs
6. ✅ Collect feedback
7. ✅ Iterate on prompts based on pilot data

---

**Your app is ready to go live! 🚀**

Follow the steps above to deploy to Streamlit Cloud in less than 10 minutes.
