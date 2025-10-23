# 🚂 Deploy to Railway

## One-Click Deploy Steps

### 1. Push to GitHub

```bash
# Initialize git (if not done)
git init

# Add all files (venv is automatically excluded)
git add .

# Commit
git commit -m "FastAPI Document Converter - Ready for deployment"

# Create main branch
git branch -M main

# Add your GitHub repository
git remote add origin https://github.com/yourusername/your-repo.git

# Push
git push -u origin main
```

### 2. Deploy on Railway

1. Go to https://railway.app
2. Login with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your repository
6. Railway automatically detects Dockerfile
7. Click "Deploy"
8. Wait ~2 minutes ⏳
9. Done! ✅

### 3. Get Your Live URL

Railway provides a URL like:
```
https://your-app-name.up.railway.app
```

Access your API:
- Docs: `https://your-app.up.railway.app/docs`
- Health: `https://your-app.up.railway.app/health`

## 🎯 That's It!

No configuration needed - Railway uses the Dockerfile automatically.

## 📝 Files for Railway

- ✅ `Dockerfile` - Tells Railway how to build
- ✅ `requirements.txt` - Python dependencies
- ✅ `.dockerignore` - Excludes venv from build
- ✅ `railway.json` - Railway config (optional)
- ✅ `.gitignore` - Excludes venv from git

## 🔄 Update Deployed App

Just push to GitHub:
```bash
git add .
git commit -m "Updates"
git push
```

Railway automatically redeploys! 🚀

## 💰 Cost

Railway offers:
- Free tier: $5 credit/month
- Enough for small projects
- Upgrade as needed

