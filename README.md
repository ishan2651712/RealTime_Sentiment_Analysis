# Project Structure and File Guide

## 📁 Folder Structure

### `/dataset/`
- **Purpose**: Contains the main dataset CSV file
- **Files**:
  - `amazon_reviews.csv`: The main dataset with Amazon product reviews
  - This file is **dynamically updated** when you save new reviews through the web app

### `/output/`
- **Purpose**: Stores analysis results from batch processing
- **Usage**: 
  - When you run batch analysis, results can be saved here
  - Currently contains `sample_results.txt` as an example
  - This folder is **optional** - batch processing results can be downloaded directly from the web app

### `/report/`
- **Purpose**: Contains project documentation and reports
- **Files**:
  - `Mini_Project_Report.docx`: Project documentation/report
  - This folder is for **documentation only** - not used by the application code

### `/models/`
- **Purpose**: Contains machine learning models and lexicons
- **Files**:
  - `sentiment_lexicon.txt`: Dictionary of positive/negative sentiment words
  - **Required** - used by the sentiment analysis system

### `/src/`
- **Purpose**: Contains all source code files
- **Files**:
  - `web_app.py`: **Main Streamlit web application** (USE THIS)
  - `app.py`: Command-line interface (optional, can be deleted if you only use web app)
  - `preprocessing.py`: Text preprocessing module
  - `feature_extraction.py`: Feature extraction module
  - `sentiment_analysis.py`: Sentiment analysis classifier

## 🔧 Key Files Explained

### `web_app.py` vs `app.py`

**`web_app.py`** (⭐ USE THIS):
- Streamlit-based web interface
- Run with: `streamlit run src/web_app.py`
- Features:
  - Interactive web UI
  - Real-time sentiment analysis
  - Save reviews to dataset
  - Batch processing with visualizations
  - Analytics dashboard

**`app.py`** (Optional):
- Command-line interface (terminal-based)
- Run with: `python src/app.py`
- Features:
  - Text-based interface
  - Same sentiment analysis capabilities
  - No web UI

**Recommendation**: 
- If you're using the web app (`web_app.py`), you **can delete `app.py`** - it's not needed
- Keep it if you want a command-line option

## 📊 How Data Flows

1. **User Input** → Web App (`web_app.py`)
2. **Analysis** → Sentiment Analyzer (`sentiment_analysis.py`)
3. **Save Review** → Updates `dataset/amazon_reviews.csv`
4. **Batch Processing** → Reads from `dataset/amazon_reviews.csv`
5. **Results** → Can be downloaded or saved to `output/` (optional)

## 🎯 Current Status

- ✅ Web app is fully functional
- ✅ Reviews can be saved to dataset (dynamically updates CSV)
- ✅ Batch processing reads current dataset count
- ✅ Analytics shows analysis history

