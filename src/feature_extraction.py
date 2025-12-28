"""
feature_extraction.py
PHASE 4: Feature Extraction Module
Extracts features from preprocessed text for sentiment analysis
"""
import nltk

# Ensure required NLTK data is available
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

from collections import Counter
import os

class FeatureExtractor:
    """
    Extracts features from preprocessed text
    """
    
    def __init__(self, lexicon_path='models/sentiment_lexicon.txt'):
        """
        Initialize feature extractor with sentiment lexicon
        """
        self.positive_words = {}
        self.negative_words = {}
        self.load_lexicon(lexicon_path)
    
    def load_lexicon(self, lexicon_path):
        """
        Load sentiment lexicon from file
        Format: word,score
        """
        if not os.path.exists(lexicon_path):
            print(f"⚠️ Warning: Lexicon file not found at {lexicon_path}")
            return
        
        with open(lexicon_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue
                
                try:
                    word, score = line.split(',')
                    score = float(score)
                    
                    if score > 0:
                        self.positive_words[word] = score
                    elif score < 0:
                        self.negative_words[word] = score
                except ValueError:
                    continue
        
        print(f"✅ Loaded {len(self.positive_words)} positive words")
        print(f"✅ Loaded {len(self.negative_words)} negative words")
    
    def extract_ngrams(self, tokens, n=2):
        """
        Extract n-grams from tokens
        
        Args:
            tokens (list): List of words
            n (int): Size of n-gram (2 for bigrams, 3 for trigrams)
            
        Returns:
            list: List of n-grams
        """
        ngrams = []
        for i in range(len(tokens) - n + 1):
            ngram = ' '.join(tokens[i:i+n])
            ngrams.append(ngram)
        return ngrams
    
    def calculate_sentiment_score(self, tokens):
        """
        Calculate sentiment score using lexicon-based approach
        
        Args:
            tokens (list): Preprocessed tokens
            
        Returns:
            dict: Sentiment features
        """
        positive_score = 0
        negative_score = 0
        positive_count = 0
        negative_count = 0
        
        # Calculate scores
        for token in tokens:
            if token in self.positive_words:
                positive_score += self.positive_words[token]
                positive_count += 1
            elif token in self.negative_words:
                negative_score += abs(self.negative_words[token])
                negative_count += 1
        
        # Total sentiment score
        total_score = positive_score - negative_score
        
        # Normalize by token count
        if len(tokens) > 0:
            normalized_score = total_score / len(tokens)
        else:
            normalized_score = 0
        
        return {
            'positive_score': positive_score,
            'negative_score': negative_score,
            'total_score': total_score,
            'normalized_score': normalized_score,
            'positive_count': positive_count,
            'negative_count': negative_count,
            'token_count': len(tokens)
        }
    
    def detect_negation(self, tokens):
        """
        Detect negation patterns in text
        """
        negation_words = {'not', 'no', 'never', 'neither', 'nor', 'none', 
                         'nobody', 'nothing', 'nowhere', "don't", "doesn't",
                         "didn't", "won't", "wouldn't", "shouldn't", "couldn't"}
        
        negation_count = sum(1 for token in tokens if token in negation_words)
        return negation_count
    
    def extract_features(self, tokens, include_ngrams=True):
        """
        Extract all features from tokens
        
        Args:
            tokens (list): Preprocessed tokens
            include_ngrams (bool): Whether to include n-grams
            
        Returns:
            dict: All extracted features
        """
        features = {}
        
        # Sentiment scores
        sentiment_features = self.calculate_sentiment_score(tokens)
        features.update(sentiment_features)
        
        # Negation detection
        features['negation_count'] = self.detect_negation(tokens)
        
        # N-grams (optional)
        if include_ngrams:
            bigrams = self.extract_ngrams(tokens, n=2)
            features['bigrams'] = bigrams
            features['bigram_count'] = len(bigrams)
        
        # Text length features
        features['word_count'] = len(tokens)
        features['avg_word_length'] = sum(len(word) for word in tokens) / len(tokens) if tokens else 0
        
        return features


def demo_feature_extraction():
    """
    Demonstration of feature extraction
    """
    print("=" * 70)
    print("FEATURE EXTRACTION DEMONSTRATION")
    print("=" * 70)
    
    # Sample preprocessed tokens
    positive_tokens = ['product', 'amazing', 'love', 'best', 'purchase']
    negative_tokens = ['terrible', 'quality', 'broke', 'waste', 'money']
    neutral_tokens = ['product', 'okay', 'works', 'fine', 'average']
    
    # Initialize feature extractor
    extractor = FeatureExtractor()
    
    print("\n" + "="*70)
    print("POSITIVE REVIEW FEATURES:")
    print("="*70)
    print(f"Tokens: {positive_tokens}")
    features = extractor.extract_features(positive_tokens)
    for key, value in features.items():
        if key != 'bigrams':
            print(f"  {key}: {value}")
    
    print("\n" + "="*70)
    print("NEGATIVE REVIEW FEATURES:")
    print("="*70)
    print(f"Tokens: {negative_tokens}")
    features = extractor.extract_features(negative_tokens)
    for key, value in features.items():
        if key != 'bigrams':
            print(f"  {key}: {value}")
    
    print("\n" + "="*70)
    print("NEUTRAL REVIEW FEATURES:")
    print("="*70)
    print(f"Tokens: {neutral_tokens}")
    features = extractor.extract_features(neutral_tokens)
    for key, value in features.items():
        if key != 'bigrams':
            print(f"  {key}: {value}")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    demo_feature_extraction()