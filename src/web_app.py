"""
web_app.py
Amazon Review Sentiment Analyzer - Dynamic Dataset System
Features: Save reviews, auto-update dataset, dynamic counting
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sentiment_analysis import SentimentAnalyzer
import os
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Sentiment Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Custom CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .main-title {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        padding: 1rem 0;
    }
    
    .subtitle {
        text-align: center;
        color: #6c757d;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    .result-card {
        padding: 2rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .result-card:hover {
        transform: translateY(-5px);
    }
    
    .positive-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .negative-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
    }
    
    .neutral-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
    }
    
    .sentiment-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    .confidence-text {
        font-size: 1.8rem;
        font-weight: 600;
        margin: 0.5rem 0;
    }
    
    .score-text {
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    .metric-container {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        text-align: center;
        margin: 0.5rem;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #667eea;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #6c757d;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .feature-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    }
    
    .feature-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 1rem;
    }
    
    .feature-text {
        color: #4a5568;
        line-height: 1.8;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.8rem 2rem;
        border-radius: 25px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    .stTextArea>div>div>textarea {
        border-radius: 15px;
        border: 2px solid #e2e8f0;
        padding: 1rem;
        font-size: 1rem;
    }
    
    .stTextArea>div>div>textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .info-box {
        background: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        margin: 1rem 0;
    }
    
    .stats-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .progress-text {
        font-size: 1.1rem;
        color: #667eea;
        font-weight: 600;
        text-align: center;
        margin: 1rem 0;
    }
    
    .save-indicator {
        background: #10b981;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        display: inline-block;
        font-weight: 600;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Dataset path - handle both relative and absolute paths
_script_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(_script_dir)
DATASET_PATH = os.path.join(_project_root, 'dataset', 'amazon_reviews.csv')

# Initialize session state
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = None
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []
if 'dataset_updated' not in st.session_state:
    st.session_state.dataset_updated = False

@st.cache_resource
def load_analyzer():
    """Load sentiment analyzer"""
    # Use absolute path for lexicon
    lexicon_path = os.path.join(_project_root, 'models', 'sentiment_lexicon.txt')
    return SentimentAnalyzer(lexicon_path=lexicon_path)

def get_dataset_count():
    """Get current count of reviews in dataset - ALWAYS reads fresh from file"""
    try:
        if os.path.exists(DATASET_PATH):
            df = pd.read_csv(DATASET_PATH)
            return len(df)
        return 0
    except Exception as e:
        print(f"ERROR reading dataset: {e}")
        return 0

def save_review_to_dataset(review_text, predicted_sentiment, confidence, rating=None):
    """Save new review to dataset"""
    try:
        # Check if file exists
        if not os.path.exists(DATASET_PATH):
            return False, f"Dataset file not found at: {DATASET_PATH}"
        
        # Load existing dataset
        df = pd.read_csv(DATASET_PATH)
        old_count = len(df)
        
        # Get next Review_ID
        if len(df) > 0:
            next_id = int(df['Review_ID'].max() + 1)
        else:
            next_id = 1
        
        # Assign rating based on sentiment if not provided
        if rating is None:
            if predicted_sentiment == 'Positive':
                rating = 5
            elif predicted_sentiment == 'Negative':
                rating = 1
            else:
                rating = 3
        
        # Create new row
        new_row = {
            'Review_ID': next_id,
            'Rating': rating,
            'Review_Text': review_text,
            'Sentiment': predicted_sentiment
        }
        
        # Append to dataframe
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        
        # Save back to CSV
        df.to_csv(DATASET_PATH, index=False)
        
        # Verify the save worked
        verify_df = pd.read_csv(DATASET_PATH)
        new_count = len(verify_df)
        
        if new_count != old_count + 1:
            return False, f"Save verification failed - expected {old_count + 1} rows but found {new_count}"
        
        print(f"✅ Saved review ID {next_id}. Total: {old_count} → {new_count}")
        return True, next_id
    except Exception as e:
        import traceback
        error_msg = f"Error: {str(e)}"
        print(f"❌ Save error: {error_msg}")
        return False, error_msg

def remove_reviews_from_dataset(review_ids):
    """Remove reviews from dataset by Review_ID"""
    try:
        if not review_ids:
            return True
        
        # Load existing dataset
        df = pd.read_csv(DATASET_PATH)
        
        # Filter out reviews with matching IDs
        df_filtered = df[~df['Review_ID'].isin(review_ids)]
        
        # Save back to CSV
        df_filtered.to_csv(DATASET_PATH, index=False)
        
        return True
    except Exception as e:
        return False

def display_result_card(result, show_save_option=True):
    """Display beautiful result card with save option"""
    sentiment = result['sentiment']
    confidence = result['confidence']
    score = result['sentiment_score']
    
    # Choose card style
    if sentiment == 'Positive':
        card_class = 'positive-card'
        emoji = '😊'
        icon = '✨'
    elif sentiment == 'Negative':
        card_class = 'negative-card'
        emoji = '😞'
        icon = '⚠️'
    else:
        card_class = 'neutral-card'
        emoji = '😐'
        icon = '📊'
    
    # Display card
    st.markdown(f"""
        <div class="result-card {card_class}">
            <div class="sentiment-title">{emoji} {sentiment} {icon}</div>
            <div class="confidence-text">Confidence: {confidence:.1f}%</div>
            <div class="score-text">Sentiment Score: {score:.4f}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Metrics in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div class="metric-container">
                <div class="metric-value">+{result['positive_words']}</div>
                <div class="metric-label">Positive Words</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric-container">
                <div class="metric-value">-{result['negative_words']}</div>
                <div class="metric-label">Negative Words</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="metric-container">
                <div class="metric-value">{result['total_words']}</div>
                <div class="metric-label">Total Words</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Save to dataset option
    if show_save_option:
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("💾 Save This Review to Dataset", key=f"save_{id(result)}", width='stretch'):
                success, result_id = save_review_to_dataset(
                    result['original_text'],
                    result['sentiment'],
                    result['confidence']
                )
                
                if success:
                    # Update existing entry in history or add new one
                    found = False
                    for idx, item in enumerate(st.session_state.analysis_history):
                        if item.get('original_text') == result['original_text']:
                            # Update existing entry
                            st.session_state.analysis_history[idx]['saved_to_dataset'] = True
                            st.session_state.analysis_history[idx]['review_id'] = result_id
                            found = True
                            break
                    
                    # If not found in history, add it
                    if not found:
                        result_copy = result.copy()
                        result_copy['saved_to_dataset'] = True
                        result_copy['review_id'] = result_id
                        st.session_state.analysis_history.append(result_copy)
                    
                    # Get updated count after save
                    updated_count = get_dataset_count()
                    st.markdown(f"""
                        <div class="save-indicator">
                            ✅ Review saved to dataset! (ID: {result_id})<br>
                            📊 Total reviews in dataset: {updated_count:,}
                        </div>
                    """, unsafe_allow_html=True)
                    st.session_state.dataset_updated = True
                    # Force immediate refresh to show updated count everywhere
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error(f"❌ Error saving review!")
                    st.error(f"Details: {result_id}")
                    st.info("💡 Check the terminal/console for detailed error messages")
    
    # Detailed Analysis
    with st.expander("🔍 Detailed Analysis & Verification"):
        st.markdown("### Original Review:")
        st.info(result['original_text'])
        
        st.markdown("### Cleaned Text:")
        st.code(result['cleaned_text'])
        
        st.markdown("### Processed Tokens:")
        st.code(', '.join(result['processed_tokens']))
        
        st.markdown("### How to Verify This Result:")
        st.success(f"""
        **Manual Verification Steps:**
        
        1. **Read the original review** - Does it feel {sentiment.lower()}?
        2. **Count positive words** - Found {result['positive_words']} positive words
        3. **Count negative words** - Found {result['negative_words']} negative words
        4. **Check the ratio** - More positive = Positive sentiment
        5. **Confidence score** - {confidence:.1f}% shows how certain we are
        
        **Expected Result:** 
        - If review has words like "amazing, great, love" → Positive ✅
        - If review has words like "terrible, worst, bad" → Negative ❌
        - If neutral words or mixed → Neutral ⚖️
        """)

def main():
    """Main application"""
    
    # Header
    st.markdown('<h1 class="main-title">🎯 Sentiment Analysis System</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Advanced NLP-Powered Amazon Review Analyzer</p>', unsafe_allow_html=True)
    
    # Initialize analyzer
    if st.session_state.analyzer is None:
        with st.spinner("🔄 Loading AI models..."):
            st.session_state.analyzer = load_analyzer()
            time.sleep(0.5)
        st.success("✅ System initialized successfully!")
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 📋 Navigation")
        page = st.radio(
            "Navigation",
            ["🏠 Home", "💬 Analyze Review", "📦 Batch Processing", "📊 Analytics"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Get fresh dataset count for sidebar
        dataset_count = get_dataset_count()
        
        st.markdown(f"""
            <div class="info-box">
                <h3 style="margin-top:0;">ℹ️ About</h3>
                <p>This system uses Natural Language Processing to analyze Amazon product reviews.</p>
                <p><strong>Current Dataset:</strong> {dataset_count:,} reviews</p>
                <p><strong>Accuracy:</strong> ~85-90%</p>
                <p><strong>Processing:</strong> Real-time</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.analysis_history:
            st.markdown(f"""
                <div class="stats-container">
                    <h4>📈 Session Stats</h4>
                    <p>Reviews analyzed: <strong>{len(st.session_state.analysis_history)}</strong></p>
                </div>
            """, unsafe_allow_html=True)
    
    # HOME PAGE
    if page == "🏠 Home":
        st.markdown("## Welcome to Advanced Sentiment Analysis")
        
        # Get fresh dataset count
        dataset_count = get_dataset_count()
        st.info(f"📊 **Current Dataset:** {dataset_count:,} reviews ready for analysis")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
                <div class="feature-card">
                    <div class="feature-title">⚡ Real-Time</div>
                    <div class="feature-text">
                        Instant sentiment detection with confidence scores
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div class="feature-card">
                    <div class="feature-title">💾 Save Reviews</div>
                    <div class="feature-text">
                        Add new reviews to dataset automatically
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
                <div class="feature-card">
                    <div class="feature-title">📊 Dynamic</div>
                    <div class="feature-text">
                        Auto-updating graphs and statistics
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("## 🚀 How It Works")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
                ### Step 1: Preprocessing
                - Clean and normalize text
                - Remove stopwords
                - Tokenize into words
                - Apply lemmatization
            """)
            
            st.markdown("""
                ### Step 2: Feature Extraction
                - Match sentiment lexicon
                - Count positive/negative words
                - Calculate sentiment scores
            """)
        
        with col2:
            st.markdown("""
                ### Step 3: Classification
                - Apply rule-based logic
                - Calculate confidence
                - Determine final sentiment
            """)
            
            st.markdown("""
                ### Step 4: Save & Update
                - Save new reviews to dataset
                - Auto-update statistics
                - Dynamic batch processing
            """)
    
    # ANALYZE REVIEW PAGE
    elif page == "💬 Analyze Review":
        st.markdown("## 💬 Analyze Your Review")
        
        # Get fresh dataset count
        dataset_count = get_dataset_count()
        st.info(f"💡 **Tip:** Analyzed reviews can be saved to dataset (currently {dataset_count:,} reviews)")
        
        # Text input
        review_text = st.text_area(
            "Enter Amazon product review:",
            height=200,
            placeholder="Example: This product is amazing! The quality is excellent and delivery was fast. Highly recommended!",
            help="Type or paste any Amazon product review to analyze its sentiment"
        )
        
        # Analyze button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🔍 Analyze Sentiment", width='stretch'):
                if review_text.strip():
                    with st.spinner("🤔 Analyzing sentiment..."):
                        time.sleep(0.5)
                        result = st.session_state.analyzer.analyze_sentiment(review_text)
                        st.session_state.analysis_history.append(result)
                    
                    # Display result
                    st.markdown("---")
                    display_result_card(result, show_save_option=True)
                    
                else:
                    st.warning("⚠️ Please enter a review first!")
        
        # Quick Examples
        st.markdown("---")
        st.markdown("### 💡 Try Quick Examples")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("😊 Positive Review", width='stretch'):
                example = "This product is absolutely amazing! The quality exceeded my expectations. Best purchase I've made this year. Highly recommend to everyone!"
                st.text_area("Example Review:", value=example, height=150, key="pos_example")
                result = st.session_state.analyzer.analyze_sentiment(example)
                st.session_state.analysis_history.append(result)
                display_result_card(result, show_save_option=True)
        
        with col2:
            if st.button("😞 Negative Review", width='stretch'):
                example = "Terrible quality! Product broke after one day. Complete waste of money. Very disappointed with this purchase. Would not recommend."
                st.text_area("Example Review:", value=example, height=150, key="neg_example")
                result = st.session_state.analyzer.analyze_sentiment(example)
                st.session_state.analysis_history.append(result)
                display_result_card(result, show_save_option=True)
        
        with col3:
            if st.button("😐 Neutral Review", width='stretch'):
                example = "It's okay. Nothing special but it works. Average quality for the price. Does what it's supposed to do."
                st.text_area("Example Review:", value=example, height=150, key="neu_example")
                result = st.session_state.analyzer.analyze_sentiment(example)
                st.session_state.analysis_history.append(result)
                display_result_card(result, show_save_option=True)
    
    # BATCH PROCESSING PAGE
    elif page == "📦 Batch Processing":
        st.markdown("## 📦 Batch Processing")
        
        # Get current count
        current_count = get_dataset_count()
        
        if not os.path.exists(DATASET_PATH):
            st.error("❌ Dataset not found!")
            return
        
        st.info(f"📊 Ready to analyze **{current_count:,} reviews** from the dataset")
        
        # Show dataset growth
        if st.session_state.dataset_updated:
            st.success("✅ Dataset updated! New reviews have been added.")
            st.session_state.dataset_updated = False
        
        if st.button("🚀 Start Batch Analysis", width='stretch'):
            # Load dataset
            df = pd.read_csv(DATASET_PATH)
            total = len(df)
            
            st.info(f"🔄 Analyzing {total:,} reviews...")
            
            # Progress tracking
            progress_bar = st.progress(0)
            status = st.empty()
            
            results = []
            correct = 0
            
            # Analyze all reviews
            for idx, row in df.iterrows():
                progress = (idx + 1) / total
                progress_bar.progress(progress)
                status.markdown(f'<p class="progress-text">Processing review {idx + 1:,} of {total:,}</p>', unsafe_allow_html=True)
                
                analysis = st.session_state.analyzer.analyze_sentiment(row['Review_Text'])
                
                is_correct = (row['Sentiment'] == analysis['sentiment'])
                if is_correct:
                    correct += 1
                
                results.append({
                    'Review_ID': row['Review_ID'],
                    'Review': row['Review_Text'][:80] + '...',
                    'Actual': row['Sentiment'],
                    'Predicted': analysis['sentiment'],
                    'Confidence': f"{analysis['confidence']:.1f}%",
                    'Match': '✅' if is_correct else '❌'
                })
            
            progress_bar.empty()
            status.empty()
            
            # Calculate metrics
            accuracy = (correct / total) * 100
            
            # Display results
            st.success(f"✅ Analysis Complete! Processed {total:,} reviews")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                    <div class="metric-container">
                        <div class="metric-value">{total:,}</div>
                        <div class="metric-label">Total Reviews</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                    <div class="metric-container">
                        <div class="metric-value">{accuracy:.1f}%</div>
                        <div class="metric-label">Accuracy</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                    <div class="metric-container">
                        <div class="metric-value">{correct:,}</div>
                        <div class="metric-label">Correct</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                    <div class="metric-container">
                        <div class="metric-value">{total - correct:,}</div>
                        <div class="metric-label">Incorrect</div>
                    </div>
                """, unsafe_allow_html=True)
            
            # Create sentiment distribution charts
            results_df = pd.DataFrame(results)
            
            st.markdown("### 📊 Sentiment Distribution")
            
            col1, col2 = st.columns(2)
            
            # Count sentiments
            actual_sentiments = df['Sentiment'].value_counts()
            predicted_sentiments = results_df['Predicted'].value_counts()
            
            with col1:
                st.markdown("**Actual Sentiments:**")
                fig1 = px.pie(
                    values=actual_sentiments.values,
                    names=actual_sentiments.index,
                    color=actual_sentiments.index,
                    color_discrete_map={'Positive': '#667eea', 'Negative': '#f5576c', 'Neutral': '#00f2fe'}
                )
                fig1.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig1, width='stretch')
            
            with col2:
                st.markdown("**Predicted Sentiments:**")
                fig2 = px.pie(
                    values=predicted_sentiments.values,
                    names=predicted_sentiments.index,
                    color=predicted_sentiments.index,
                    color_discrete_map={'Positive': '#667eea', 'Negative': '#f5576c', 'Neutral': '#00f2fe'}
                )
                fig2.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig2, width='stretch')
            
            # Show sample results
            st.markdown("### 📋 Sample Results (First 50)")
            st.dataframe(results_df.head(50), width='stretch')
            
            # Download button
            csv = results_df.to_csv(index=False)
            st.download_button(
                "📥 Download Full Results",
                data=csv,
                file_name=f"sentiment_analysis_{total}_reviews.csv",
                mime="text/csv",
                width='stretch'
            )
    
    # ANALYTICS PAGE
    elif page == "📊 Analytics":
        st.markdown("## 📊 Analytics Dashboard")
        
        # Show dataset info
        st.info(f"📊 **Dataset Status:** {dataset_count:,} reviews in database")
        
        if not st.session_state.analysis_history:
            st.info("📭 No analysis data yet. Analyze some reviews first!")
        else:
            history = st.session_state.analysis_history
            
            # Sentiment distribution
            sentiments = [item['sentiment'] for item in history]
            df_sent = pd.DataFrame({'Sentiment': sentiments})
            counts = df_sent['Sentiment'].value_counts()
            
            # Create pie chart
            fig = px.pie(
                values=counts.values,
                names=counts.index,
                title=f"Sentiment Distribution ({len(history)} reviews analyzed)",
                color=counts.index,
                color_discrete_map={
                    'Positive': '#667eea',
                    'Negative': '#f5576c',
                    'Neutral': '#00f2fe'
                },
                hole=0.4
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(height=500)
            
            st.plotly_chart(fig, width='stretch')
            
            # History table
            st.markdown("### 📜 Analysis History")
            
            history_data = []
            for i, item in enumerate(reversed(history[-20:]), 1):
                history_data.append({
                    '#': i,
                    'Review': item['original_text'][:60] + '...',
                    'Sentiment': item['sentiment'],
                    'Confidence': f"{item['confidence']:.1f}%"
                })
            
            st.dataframe(pd.DataFrame(history_data), width='stretch')
            
            # Clear history
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🗑️ Clear Session History", width='stretch'):
                    # Get review IDs that were saved to dataset
                    saved_review_ids = [
                        item.get('review_id') 
                        for item in st.session_state.analysis_history 
                        if item.get('saved_to_dataset') and item.get('review_id')
                    ]
                    
                    # Remove saved reviews from dataset CSV
                    if saved_review_ids:
                        remove_reviews_from_dataset(saved_review_ids)
                    
                    # Clear analysis history
                    st.session_state.analysis_history = []
                    st.session_state.dataset_updated = True
                    st.rerun()
            
            with col2:
                if st.button("🔄 Refresh Dashboard", width='stretch'):
                    st.rerun()

if __name__ == "__main__":
    main()