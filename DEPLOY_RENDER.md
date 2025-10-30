# Deploy to Render (Free Plan)

This guide will help you deploy the Chess Tournament Monitor to Render's free plan.

## Prerequisites

- A GitHub account
- A Render account (sign up at https://render.com)
- Your code pushed to a GitHub repository

## Deployment Steps

### 1. Push Your Code to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Chess Tournament Monitor"

# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Push to GitHub
git push -u origin master
```

### 2. Create a New Web Service on Render

1. Go to https://dashboard.render.com
2. Click "New +" button and select "Web Service"
3. Connect your GitHub repository
4. Configure the service:

   **Basic Settings:**
   - Name: `chess-tournament-monitor` (or your preferred name)
   - Region: Choose the closest to your location
   - Branch: `master` (or your main branch)
   - Root Directory: Leave empty (unless your app is in a subdirectory)

   **Build & Deploy Settings:**
   - Runtime: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120`

   **Plan:**
   - Select: `Free` (this is what you need!)

5. Click "Create Web Service"

### 3. Environment Variables (Optional)

If you need to configure any environment variables:

1. Go to your service dashboard
2. Navigate to "Environment" tab
3. Add variables:
   - `PYTHON_VERSION`: `3.11.0` (optional, Render auto-detects)
   - `DEBUG`: `False` (recommended for production)

### 4. Deployment

- Render will automatically:
  - Install dependencies from `requirements.txt`
  - Start your app using the command in `Procfile` or the start command you specified
  - Assign a public URL like: `https://your-app-name.onrender.com`

- The deployment process takes 2-5 minutes
- Watch the logs in real-time from the Render dashboard

### 5. Access Your App

Once deployed, your app will be available at:
```
https://your-app-name.onrender.com
```

**Main endpoints:**
- Home page: `https://your-app-name.onrender.com/`
- View all sessions: `https://your-app-name.onrender.com/view`
- API: `https://your-app-name.onrender.com/api/sessions`

## Important Notes for Render Free Plan

### Limitations:
1. **Service sleeps after 15 minutes of inactivity**
   - First request after sleep takes 30-60 seconds to wake up
   - This is normal for free tier

2. **750 hours/month free**
   - If you need 24/7 uptime, consider upgrading
   - For occasional use, free tier is perfect

3. **No persistent storage**
   - Data is stored in memory only
   - All sessions are lost when service restarts
   - This app doesn't need persistence anyway

4. **Automatic deploys**
   - Every push to your GitHub branch triggers a new deployment
   - Takes 2-5 minutes per deployment

### Configuration Files Included:

1. **`render.yaml`** - Render Blueprint configuration (optional)
2. **`Procfile`** - Tells Render how to start your app
3. **`requirements.txt`** - Python dependencies (includes gunicorn)
4. **Updated `app.py`** - Reads PORT from environment variable

## Troubleshooting

### App Won't Start
- Check logs in Render dashboard
- Verify all dependencies in `requirements.txt`
- Ensure `gunicorn` is installed

### Port Issues
- Render automatically sets `PORT` environment variable
- App is configured to read from `os.environ.get("PORT", 8080)`
- Don't hardcode port numbers

### Cold Starts (Service Sleeping)
- Free tier sleeps after 15 minutes of inactivity
- First request takes 30-60 seconds to wake up
- Consider upgrading to paid plan for always-on service

### Sessions Lost After Restart
- This is expected behavior
- App stores sessions in memory
- Use external database if you need persistence

## Monitoring

### View Logs
1. Go to Render dashboard
2. Select your service
3. Click "Logs" tab
4. See real-time application logs

### Check Status
- Dashboard shows service status: `Live`, `Building`, `Failed`
- CPU and memory usage graphs
- Request metrics

## Updating Your App

```bash
# Make changes to your code
git add .
git commit -m "Update feature"
git push

# Render automatically deploys the changes
```

## Alternative: Manual Deploy

If you prefer not to use GitHub auto-deploy:

1. Use Render Blueprint (`render.yaml` included)
2. Or deploy from Render dashboard manually

## Cost

- **Free tier**: $0/month
- **Starter tier**: $7/month (if you need always-on service)

## Security Notes

1. Don't commit sensitive data
2. Use environment variables for secrets
3. Keep `.env` files in `.gitignore`
4. Render's free tier uses HTTPS by default

## Support

- Render Docs: https://render.com/docs
- Render Community: https://community.render.com
- App Issues: Check your GitHub repository

## Next Steps

1. Deploy to Render using steps above
2. Test all endpoints
3. Share the URL with users
4. Monitor usage and logs

Happy monitoring! ♟️
