# 🚂 Railway Deployment Guide

Deploy your FastAPI Document Converter to Railway with zero configuration needed!

## 🚀 Quick Deploy to Railway

### Prerequisites
- GitHub account
- Railway account (https://railway.app)

### Steps

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: FastAPI Document Converter"
   git branch -M main
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Deploy on Railway**
   - Go to https://railway.app
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway will automatically detect the Dockerfile and deploy!

3. **That's it!** 🎉
   - Railway automatically uses the Dockerfile
   - No configuration needed
   - Your API will be live at: `https://your-app.up.railway.app`

## 📋 What's Included

✅ **Dockerfile** - Optimized for production
✅ **railway.json** - Railway configuration
✅ **railway.toml** - Alternative config format
✅ **.dockerignore** - Excludes unnecessary files
✅ **.gitignore** - Hides venv and sensitive files

## 🔧 Configuration Files

### Dockerfile
- Uses Python 3.12 slim image
- Installs all dependencies
- Exposes port 8000 (Railway auto-assigns)
- Includes health check
- Production-ready settings

### railway.json / railway.toml
- Specifies Dockerfile build
- Sets start command
- Configures restart policy

### .dockerignore
- Excludes venv, logs, uploads from Docker build
- Keeps Docker image small and fast

## 🌍 Environment Variables (Optional)

If you need to set environment variables on Railway:

1. Go to your Railway project
2. Click "Variables" tab
3. Add variables:
   - `APP_NAME` = "FastAPI Document Converter"
   - `DEBUG` = "False"
   - `LOG_LEVEL` = "INFO"
   - (Optional) Add any custom settings

Railway automatically provides:
- `PORT` - Port number to use
- Other Railway-specific variables

## 🔗 Your Live API

After deployment, your API will be available at:
```
https://your-app-name.up.railway.app
```

Endpoints:
- `https://your-app.up.railway.app/docs` - API Documentation
- `https://your-app.up.railway.app/health` - Health Check
- `https://your-app.up.railway.app/api/v1/documents/docx-to-pdf` - DOCX to PDF

## 📊 Monitoring

Railway provides:
- ✅ Build logs
- ✅ Deployment logs
- ✅ Runtime metrics
- ✅ Automatic restarts
- ✅ Health checks

## 🔄 Updates

To update your deployed app:

```bash
# Make changes to your code
# Commit and push
git add .
git commit -m "Update: description of changes"
git push

# Railway automatically redeploys!
```

## 🐳 Test Docker Locally (Optional)

Before deploying, test Docker locally:

```bash
# Build image
docker build -t fastapi-converter .

# Run container
docker run -p 8000:8000 fastapi-converter

# Test
curl http://localhost:8000/health
```

## ✅ Checklist Before Deploy

- [ ] Code pushed to GitHub
- [ ] .gitignore excludes venv/
- [ ] Dockerfile is present
- [ ] requirements.txt is up to date
- [ ] App works locally
- [ ] Railway account ready

## 🎯 Railway Advantages

✅ **Zero Configuration** - Just connect GitHub  
✅ **Automatic Deploys** - Push to deploy  
✅ **Free Tier** - Great for testing  
✅ **Fast Deployments** - Usually < 2 minutes  
✅ **Automatic HTTPS** - Free SSL certificate  
✅ **Environment Variables** - Easy to manage  

## 🆘 Troubleshooting

**Build fails?**
- Check Dockerfile syntax
- Verify requirements.txt has all dependencies
- Check Railway build logs

**App crashes?**
- Check Railway runtime logs
- Verify PORT environment variable is used
- Check health endpoint

**Slow performance?**
- Upgrade Railway plan for more resources
- Optimize your conversion code
- Add caching if needed

## 📝 Notes

- Railway automatically sets the PORT environment variable
- The Dockerfile uses `${PORT:-8000}` to use Railway's port or default to 8000
- Health check helps Railway know when app is ready
- Auto-restart policy handles crashes gracefully

## 🎉 Ready to Deploy!

Your app is configured for Railway deployment with:
- ✅ Dockerfile optimized
- ✅ Railway configs added
- ✅ .gitignore configured
- ✅ .dockerignore configured

Just push to GitHub and deploy on Railway! 🚀

