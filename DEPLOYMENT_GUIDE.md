# 🚀 Deployment Guide: GitHub + Streamlit Cloud

## Step 1: Prepare Your Code for GitHub

### 1.1 Create a `.gitignore` file (if not exists)

This prevents unnecessary files from being uploaded to GitHub.

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.venv

# Streamlit
.streamlit/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Dataset (optional - you may want to exclude large CSV files)
# dataset/*.csv
# Uncomment above line if your dataset is too large for GitHub
```

### 1.2 Create a `requirements.txt` (if not exists or update it)

Make sure it has all dependencies:

```txt
streamlit>=1.28.0
pandas>=1.5.0
plotly>=5.14.0
nltk>=3.8.0
```

### 1.3 Check your file structure

Your project should look like this:

```
RealTime_Sentiment_Analysis/
├── dataset/
│   └── amazon_reviews.csv
├── models/
│   └── sentiment_lexicon.txt
├── src/
│   ├── web_app.py          (Main file - Streamlit will run this)
│   ├── preprocessing.py
│   ├── feature_extraction.py
│   └── sentiment_analysis.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Step 2: Upload to GitHub

### 2.1 Create a GitHub Repository

1. Go to [github.com](https://github.com) and sign in
2. Click the **"+"** icon in the top right → **"New repository"**
3. Fill in:
   - **Repository name**: `RealTime_Sentiment_Analysis` (or your choice)
   - **Description**: "Real-time sentiment analysis of Amazon product reviews"
   - **Visibility**: Choose Public (required for free Streamlit Cloud) or Private
   - **DO NOT** check "Initialize with README" (you already have files)
4. Click **"Create repository"**

### 2.2 Upload Files to GitHub

#### Option A: Using GitHub Website (Easiest)

1. On the new repository page, you'll see "uploading an existing file" link
2. Click **"uploading an existing file"**
3. Drag and drop all your project folders and files:
   - `dataset/` folder
   - `models/` folder
   - `src/` folder
   - `requirements.txt`
   - `README.md`
   - `.gitignore`
4. Scroll down, add commit message: "Initial commit"
5. Click **"Commit changes"**

#### Option B: Using Git Command Line (Advanced)

```bash
# Navigate to your project folder
cd /Users/alisha/Documents/Personal/ishan/RealTime_Sentiment_Analysis

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit"

# Add remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/RealTime_Sentiment_Analysis.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### 2.3 Verify Upload

- Go to your GitHub repository page
- Check that all files are there (dataset/, models/, src/, requirements.txt, etc.)

---

## Step 3: Deploy on Streamlit Cloud

### 3.1 Go to Streamlit Cloud

1. Visit [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your **GitHub account** (click "Continue with GitHub")
3. Authorize Streamlit Cloud to access your GitHub repositories

### 3.2 Deploy Your App

1. Click **"New app"** button
2. Fill in the form:

   **Repository**: Select your repository (`YOUR_USERNAME/RealTime_Sentiment_Analysis`)

   **Branch**: `main` (or `master` depending on your default branch)

   **Main file path**: `src/web_app.py`

   **App URL** (optional): Choose a custom URL like `sentiment-analysis-app` (or leave default)

3. **Advanced settings** (click to expand):

   - **Python version**: Leave as default (Python 3.11) or select Python 3.11
   - **Secrets**: Leave empty (not needed for this project)
   - **Dependencies file**: Leave as `requirements.txt` (default)
   - **Working directory**: Leave empty (defaults to repository root)
   - **Command line arguments**: Leave empty (not needed)

4. Click **"Deploy!"**

### 3.2.1 Advanced Settings Explained

**For this project, you can leave all advanced settings as default:**

- **Python version**: Default (Python 3.11) ✅

  - Your code works with Python 3.11, which is the default

- **Secrets**: Leave empty ✅

  - You don't need API keys or secrets for this project

- **Dependencies file**: `requirements.txt` ✅

  - This is already set correctly

- **Working directory**: Leave empty ✅

  - Streamlit will run from the repository root, which is correct
  - Your paths in code already handle this

- **Command line arguments**: Leave empty ✅
  - Not needed for this app

### 3.3 Wait for Deployment

- Streamlit will automatically:
  - Install dependencies from `requirements.txt`
  - Run your app
  - This takes 1-2 minutes

### 3.4 Check for Errors

- If deployment fails, check the logs in the Streamlit Cloud dashboard
- Common issues:
  - Missing dependencies in `requirements.txt`
  - Wrong file path (should be `src/web_app.py`)
  - Path issues in code (should use relative paths or absolute paths correctly)

### 3.5 Your App is Live! 🎉

- You'll get a URL like: `https://sentiment-analysis-app.streamlit.app`
- Share this URL with others
- The app automatically redeploys when you push changes to GitHub

---

## Step 4: Fix Common Issues

### Issue 1: Dataset File Not Found

**Problem**: The app can't find `amazon_reviews.csv`

**Solution**: Make sure `dataset/amazon_reviews.csv` is uploaded to GitHub

- Check file size (GitHub has limits)
- If file is too large, use Git LFS or host it elsewhere

### Issue 2: Path Errors

**Problem**: Path issues on Streamlit Cloud

**Solution**: Your current code already uses absolute paths, which should work. If issues persist:

- Streamlit Cloud runs from project root
- Path `src/web_app.py` is correct
- Internal paths in code should work with current implementation

### Issue 3: Missing Dependencies

**Problem**: ModuleNotFoundError

**Solution**:

- Check `requirements.txt` has all packages
- Common missing ones: `nltk`, `plotly`, `pandas`, `streamlit`
- Streamlit Cloud installs from `requirements.txt` automatically

### Issue 4: NLTK Data Download

**Problem**: NLTK can't download wordnet data

**Solution**: Add this to your `web_app.py` or create a setup script:

```python
import nltk
nltk.download('wordnet', quiet=True)
nltk.download('stopwords', quiet=True)
```

---

## Step 5: Update Your README.md

Add deployment info to your README:

````markdown
## 🌐 Live Demo

Try the app live: [Your Streamlit Cloud URL]

## 📦 Deployment

This app is deployed on Streamlit Cloud and automatically updates when code is pushed to the main branch.

### To deploy locally:

```bash
streamlit run src/web_app.py
```
````

```

---

## Quick Checklist

Before deploying:
- ✅ All files are in GitHub
- ✅ `requirements.txt` exists and has all dependencies
- ✅ `.gitignore` is present (optional but recommended)
- ✅ `src/web_app.py` is the main file
- ✅ Dataset file is uploaded (if needed for deployment)
- ✅ Paths in code work correctly

After deploying:
- ✅ App loads without errors
- ✅ All pages work (Home, Analyze, Batch Processing, Analytics)
- ✅ Dataset loads correctly
- ✅ Can analyze reviews
- ✅ Can save reviews (if enabled)

---

## Need Help?

- **Streamlit Cloud Docs**: [docs.streamlit.io/streamlit-community-cloud](https://docs.streamlit.io/streamlit-community-cloud)
- **GitHub Docs**: [docs.github.com](https://docs.github.com)
- Check deployment logs in Streamlit Cloud dashboard for specific errors

```
