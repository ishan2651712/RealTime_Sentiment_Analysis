"""
preprocessing.py
PHASE 3: Data Preprocessing Module
This module handles all text preprocessing tasks for sentiment analysis
"""

import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer

# Download required NLTK data (run once)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# 🔴 FIX ADDED HERE (VERY IMPORTANT)
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
    
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

class TextPreprocessor:
    """
    Handles all text preprocessing operations
    """
    
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()
        
        # Remove negation words from stopwords (important for sentiment)
        negation_words = {'no', 'not', 'nor', 'never', "don't", "doesn't", 
                         "didn't", "won't", "wouldn't", "shouldn't", "couldn't"}
        self.stop_words = self.stop_words - negation_words
    
    def clean_text(self, text):
        """
        Step 1: Clean the raw text
        - Convert to lowercase
        - Remove special characters
        - Remove extra spaces
        """
        text = text.lower()
        text = re.sub(r'http\S+|www\S+|https\S+', '', text)
        text = re.sub(r'\S+@\S+', '', text)
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def tokenize(self, text):
        """
        Step 2: Tokenization
        """
        tokens = word_tokenize(text)
        return tokens
    
    def remove_stopwords(self, tokens):
        """
        Step 3: Remove stopwords
        """
        filtered_tokens = [word for word in tokens if word not in self.stop_words]
        return filtered_tokens
    
    def stem_tokens(self, tokens):
        """
        Step 4: Stemming
        """
        stemmed_tokens = [self.stemmer.stem(word) for word in tokens]
        return stemmed_tokens
    
    def lemmatize_tokens(self, tokens):
        """
        Step 5: Lemmatization
        """
        lemmatized_tokens = [self.lemmatizer.lemmatize(word) for word in tokens]
        return lemmatized_tokens
    
    def preprocess(self, text, use_stemming=False, use_lemmatization=True):
        """
        Complete preprocessing pipeline
        """
        cleaned_text = self.clean_text(text)
        tokens = self.tokenize(cleaned_text)
        filtered_tokens = self.remove_stopwords(tokens)
        
        if use_stemming:
            processed_tokens = self.stem_tokens(filtered_tokens)
        elif use_lemmatization:
            processed_tokens = self.lemmatize_tokens(filtered_tokens)
        else:
            processed_tokens = filtered_tokens
        
        return cleaned_text, tokens, processed_tokens


def demo_preprocessing():
    """
    Demonstration of preprocessing pipeline
    """
    print("=" * 70)
    print("TEXT PREPROCESSING DEMONSTRATION")
    print("=" * 70)
    
    sample_review = "This product is AMAZING!!! I absolutely LOVE it. Best purchase ever! ❤️"
    print(f"\n📝 Original Text:\n{sample_review}")
    
    preprocessor = TextPreprocessor()
    
    cleaned = preprocessor.clean_text(sample_review)
    print(f"\n1️⃣ After Cleaning:\n{cleaned}")
    
    tokens = preprocessor.tokenize(cleaned)
    print(f"\n2️⃣ After Tokenization:\n{tokens}")
    
    filtered = preprocessor.remove_stopwords(tokens)
    print(f"\n3️⃣ After Removing Stopwords:\n{filtered}")
    
    lemmatized = preprocessor.lemmatize_tokens(filtered)
    print(f"\n4️⃣ After Lemmatization:\n{lemmatized}")
    
    cleaned_text, tokens, processed_tokens = preprocessor.preprocess(sample_review)
    print(f"\n✅ Processed Tokens: {processed_tokens}")
    print(f"\n✅ Processed Text: {' '.join(processed_tokens)}")


if __name__ == "__main__":
    demo_preprocessing()
