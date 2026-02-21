# Streamlit Cloud Deployment Guide

## Prerequisites

1. **GitHub Account** - Your code is already on GitHub ✓
2. **Streamlit Account** - Free tier at [streamlit.io](https://streamlit.io)

## Step-by-Step Deployment

### 1. Create a Streamlit Community Cloud Account

- Go to [share.streamlit.io](https://share.streamlit.io)
- Click "Sign up"
- Connect with your GitHub account
- Authorize Streamlit to access your repositories

### 2. Deploy Your Dashboard

1. In Streamlit Cloud, click **"New app"**
2. Select:
   - **Repository**: `jjdlabee/Comp3610BigDataAssingment`
   - **Branch**: `main`
   - **Main file path**: `app.py`
3. Click **"Deploy!"**

Your app will start deploying. This takes 2-3 minutes.

### 3. Share Your Dashboard URL

Once deployed, your dashboard will be live at:
```
https://comp3610bigdataassingment-<unique-id>.streamlit.app
```

You'll see this URL in Streamlit Cloud's console.

## Troubleshooting

**"requirements.txt not found"**
- Verify `requirements.txt` is at project root (not in a subfolder)
- Currently located: ✓ Root directory

**"data not loading" error**
- The dashboard expects `data/processed/taxi_summary.parquet`
- Run the `assignment1.ipynb` notebook locally first to generate this file
- The parquet file will be generated in `/data/processed/`

**Dashboard shows "FileNotFoundError"**
- .gitignore correctly excludes data files (they're generated, not committed)
- Solution: Generate data locally by running notebook, then upload parquet to repository OR
- Create a data generation job in cloud (advanced)

## Local Testing Before Cloud Deployment

Before pushing to production, test locally:

```bash
# Activate venv
.venv\Scripts\activate

# Run dashboard
streamlit run app.py

# Open browser to http://localhost:8501
```

Verify all filters and visualizations work before deploying.

## Important Notes

✓ `app.py` is at project root  
✓ `requirements.txt` includes all dependencies  
✓ `.gitignore` excludes data files (correct - they're generated)  
✓ README.md has setup instructions  

**Data file handling:**
- The parquet file must exist for dashboard to work
- Since data is large (~100MB), it's excluded from git
- Solution: Either commit `data/processed/taxi_summary.parquet` (not recommended) OR let users generate it by running the notebook

## Getting Your Dashboard URL

After deployment completes:
1. Streamlit Cloud shows the live URL
2. Copy it and provide to your instructor
3. Format: `https://comp3610bigdataassingment-<unique-id>.streamlit.app`

---

**Estimated Deployment Time**: 2-3 minutes
**Status**: Ready for deployment ✓
