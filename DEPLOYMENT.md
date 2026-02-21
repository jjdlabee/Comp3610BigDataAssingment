# Streamlit Cloud Deployment Guide

## Key Change: No Pre-Generated Data Needed

The dashboard (`app.py`) now **automatically downloads and processes data on-the-fly**. The processed parquet file is no longer required, making deployment seamless.

## Prerequisites

1. **GitHub Account** - Your code is already on GitHub ✓
2. **Streamlit Account** - Free tier at [streamlit.io](https://streamlit.io)

## How It Works

When you deploy to Streamlit Cloud:
1. App loads from `app.py`
2. Data is downloaded from official NYC Taxi Commission source (1.9M trip records)
3. Data is cleaned and aggregated (removes nulls, invalid fares, temporal anomalies)
4. Results are cached with `@st.cache_data` so processing only happens once
5. Dashboard becomes available with all filters and visualizations

**First load**: ~3-5 minutes (data download + processing)  
**Subsequent loads**: Instant (cached data)

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

Your app will start deploying. First initialization takes 3-5 minutes.

### 3. Share Your Dashboard URL

Once deployed, your dashboard will be live at:
```
https://comp3610bigdataassingment-<unique-id>.streamlit.app
```

## Local Testing Before Cloud Deployment

Test the refactored app locally first:

```bash
# Activate venv
.venv\Scripts\activate

# Run dashboard (will download data on first run)
streamlit run app.py

# Open browser to http://localhost:8501
```

Expected behavior:
- First run shows "Loading and processing taxi data..." spinner
- Data downloads from URL (~500MB)
- Cleaning and aggregation happens (~2-3 minutes)
- Dashboard displays with all 5 visualizations and filters
- Subsequent app restarts use cached data (instant)

## What's Different from Before

| Aspect | Before | Now |
|--------|--------|-----|
| Data source | Pre-generated parquet file | Downloads live from NYC TLC |
| Git tracking | Large parquet file (100MB+) | Only code files |
| First run | Instant (uses cached file) | 3-5 minutes (processing) |
| Deployment | Requires data file in repo | Works without any data files |
| Reproducibility | Depends on exact parquet version | Always uses latest Jan 2024 data |

## Troubleshooting

**Dashboard shows "Loading..." spinner for long time**
- First run downloads 1.9M trip records - this is normal (2-3 minutes)
- Subsequent loads are instant (cached)

**"HTTPSConnectionPool" or download error**
- NYC TLC server might be temporarily unavailable
- Wait a few minutes and refresh

**"FileNotFoundError" for taxi_zone_lookup.csv**
- Zone lookup is now downloaded automatically
- No longer needs to be pre-downloaded

**Memory issues on Streamlit Cloud**
- Cloud tiers have memory limits
- Data aggregation and caching should be within free tier limits (~1GB)
- All data is processed in memory then cached

## No Data Files in Repository

✓ `.gitignore` correctly excludes `data/` folder  
✓ Repository contains only source code  
✓ Data is generated dynamically by the app  
✓ Clean repository without large binary files  

## Getting Your Dashboard URL

After deployment completes:
1. Streamlit Cloud shows the live URL
2. Copy it and provide to your instructor
3. Format: `https://comp3610bigdataassingment-<unique-id>.streamlit.app`

---

**Estimated First Deployment**: 5-10 minutes total  
**First Data Load**: 3-5 minutes  
**Subsequent Loads**: Instant (~1 second)  
**Status**: Ready for deployment ✓
