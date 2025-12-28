"""
sentiment_analysis.py
PHASE 5: Sentiment Analysis Module
Main sentiment classification logic using rule-based approach
"""

from preprocessing import TextPreprocessor
from feature_extraction import FeatureExtractor
import pandas as pd

class SentimentAnalyzer:
    """
    Performs sentiment analysis on text using lexicon-based approach
    """
    
    def __init__(self, lexicon_path='models/sentiment_lexicon.txt'):
        """
        Initialize sentiment analyzer
        """
        self.preprocessor = TextPreprocessor()
        self.feature_extractor = FeatureExtractor(lexicon_path)
        
        # Sentiment thresholds
        self.positive_threshold = 0.05
        self.negative_threshold = -0.05
    
    def analyze_sentiment(self, text):
        """
        Analyze sentiment of a single text
        
        Args:
            text (str): Review text
            
        Returns:
            dict: Sentiment analysis results
        """
        # Preprocess text
        cleaned_text, tokens, processed_tokens = self.preprocessor.preprocess(text)
        
        # Extract features
        features = self.feature_extractor.extract_features(processed_tokens)
        
        # Classify sentiment based on normalized score
        normalized_score = features['normalized_score']
        
        if normalized_score > self.positive_threshold:
            sentiment = "Positive"
            confidence = min(normalized_score * 100, 100)
        elif normalized_score < self.negative_threshold:
            sentiment = "Negative"
            confidence = min(abs(normalized_score) * 100, 100)
        else:
            sentiment = "Neutral"
            confidence = 50
        
        # Adjust confidence based on word counts
        if features['positive_count'] > 0 or features['negative_count'] > 0:
            confidence = min(confidence + 20, 100)
        
        return {
            'original_text': text,
            'cleaned_text': cleaned_text,
            'processed_tokens': processed_tokens,
            'sentiment': sentiment,
            'confidence': round(confidence, 2),
            'sentiment_score': round(normalized_score, 4),
            'positive_words': features['positive_count'],
            'negative_words': features['negative_count'],
            'total_words': features['token_count']
        }
    
    def analyze_dataset(self, csv_path, output_path=None):
        """
        Analyze sentiment for entire dataset
        
        Args:
            csv_path (str): Path to CSV file
            output_path (str): Path to save results (optional)
            
        Returns:
            DataFrame: Results with sentiment predictions
        """
        print("=" * 70)
        print("ANALYZING DATASET")
        print("=" * 70)
        
        # Load dataset
        print(f"\n📂 Loading dataset from: {csv_path}")
        df = pd.read_csv(csv_path)
        print(f"✅ Loaded {len(df)} reviews")
        
        # Analyze each review
        print("\n🔄 Analyzing sentiments...")
        results = []
        
        for idx, row in df.iterrows():
            review_text = row['Review_Text']
            actual_sentiment = row['Sentiment']
            
            # Analyze sentiment
            analysis = self.analyze_sentiment(review_text)
            
            results.append({
                'Review_ID': row['Review_ID'],
                'Rating': row['Rating'],
                'Review_Text': review_text,
                'Actual_Sentiment': actual_sentiment,
                'Predicted_Sentiment': analysis['sentiment'],
                'Confidence': analysis['confidence'],
                'Sentiment_Score': analysis['sentiment_score'],
                'Positive_Words': analysis['positive_words'],
                'Negative_Words': analysis['negative_words']
            })
            
            # Progress update
            if (idx + 1) % 500 == 0:
                print(f"  Processed {idx + 1}/{len(df)} reviews...")
        
        print(f"✅ Analysis complete!")
        
        # Create results dataframe
        results_df = pd.DataFrame(results)
        
        # Save results if output path provided
        if output_path:
            results_df.to_csv(output_path, index=False)
            print(f"\n💾 Results saved to: {output_path}")
        
        # Calculate accuracy
        correct_predictions = (results_df['Actual_Sentiment'] == results_df['Predicted_Sentiment']).sum()
        accuracy = (correct_predictions / len(results_df)) * 100
        
        print("\n" + "=" * 70)
        print("ANALYSIS SUMMARY")
        print("=" * 70)
        print(f"Total Reviews: {len(results_df)}")
        print(f"Correct Predictions: {correct_predictions}")
        print(f"Accuracy: {accuracy:.2f}%")
        
        # Sentiment distribution
        print("\n📊 Predicted Sentiment Distribution:")
        sentiment_counts = results_df['Predicted_Sentiment'].value_counts()
        for sentiment, count in sentiment_counts.items():
            print(f"  {sentiment}: {count} ({count/len(results_df)*100:.1f}%)")
        
        print("=" * 70)
        
        return results_df
    
    def get_sample_predictions(self, results_df, n=10):
        """
        Get sample predictions for display
        
        Args:
            results_df (DataFrame): Results dataframe
            n (int): Number of samples
            
        Returns:
            DataFrame: Sample predictions
        """
        return results_df.head(n)


def demo_sentiment_analysis():
    """
    Demonstration of sentiment analysis
    """
    print("=" * 70)
    print("SENTIMENT ANALYSIS DEMONSTRATION")
    print("=" * 70)
    
    # Sample reviews
    reviews = [
        "This product is absolutely amazing! I love it so much!",
        "Terrible quality. Completely waste of money. Very disappointed.",
        "It's okay. Nothing special but it works fine.",
        "Best purchase ever! Highly recommend to everyone!",
        "Horrible experience. Product broke after one day."
    ]
    
    # Initialize analyzer
    analyzer = SentimentAnalyzer()
    
    print("\n" + "="*70)
    print("ANALYZING SAMPLE REVIEWS:")
    print("="*70)
    
    for i, review in enumerate(reviews, 1):
        print(f"\n{i}. Review: {review}")
        result = analyzer.analyze_sentiment(review)
        print(f"   Sentiment: {result['sentiment']}")
        print(f"   Confidence: {result['confidence']:.2f}%")
        print(f"   Score: {result['sentiment_score']:.4f}")
        print(f"   Positive Words: {result['positive_words']}")
        print(f"   Negative Words: {result['negative_words']}")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    demo_sentiment_analysis()