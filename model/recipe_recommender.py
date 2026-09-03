"""
Machine Learning (ML) Recipe Recommendation Engine featuring NLP Core.
Leverages Natural Language Processing (NLP) for deep text normalization (Stemming, Tokenization)
and ML algorithms—specifically Term Frequency-Inverse Document Frequency (TF-IDF) 
vectorization coupled with Cosine Similarity matrices—to compute semantic closeness 
between the user's querying ingredients and a large-scale recipe corpus.
"""

import pandas as pd
import nltk
import re
import os

from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

try:
    stop_words = set(stopwords.words("english"))
except LookupError:
    nltk.download("stopwords")
    stop_words = set(stopwords.words("english"))

from nltk.stem import PorterStemmer
stemmer = PorterStemmer()

DATA_PATH = "datasets/recipes.csv"

if not os.path.exists(DATA_PATH):
    raise FileNotFoundError("Dataset not found: datasets/recipes.csv")

df = pd.read_csv(DATA_PATH)

if 'Title' not in df.columns or 'Ingredients' not in df.columns:
    if 'title' in df.columns and 'ingredients' in df.columns:
        df = df.rename(columns={'title': 'Title', 'ingredients': 'Ingredients'})
    else:
        raise ValueError(
            "CSV columns do not match required columns: 'Title' and 'Ingredients'"
        )

df = df[['Title', 'Ingredients', 'Instructions']].dropna().reset_index(drop=True)

def preprocess_text(text):
    """
    NLP Tokenization Data Pipeline:
    Sanitizes string token inputs. Normalizes casing, strips non-alphabetic characters, 
    delegates stopwords, and performs NLP algorithmic stemming to isolate root word signals.
    """
    text = str(text).lower()
    text = re.sub(r'[^a-z\s]', '', text)

    tokens = text.split()
    tokens = [stemmer.stem(word) for word in tokens if word not in stop_words]

    return " ".join(tokens)

df['clean_ingredients'] = df['Ingredients'].apply(preprocess_text)

vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2)
)
tfidf_matrix = vectorizer.fit_transform(df['clean_ingredients'])

def recommend_recipe(user_input):
    """
    ML/NLP Hybrid Scoring Engine:
    Computes Machine Learning TF-IDF matrix similarity overlaid with dynamic NLP 
    overlap ratio heuristics to return the singular best mathematical recipe match.
    """
    if not user_input or user_input.strip() == "":
        return None

    user_input_clean = preprocess_text(user_input)
    if not user_input_clean:
        return None

    user_words = set(user_input_clean.split())
    if not user_words:
        return None

    user_vec = vectorizer.transform([user_input_clean])
    similarity_scores = cosine_similarity(user_vec, tfidf_matrix).flatten()
    
    best_score = -1
    best_index = -1
    
    for i, row in df.iterrows():
        recipe_ing_str = row['clean_ingredients']
        if not recipe_ing_str:
            continue
            
        recipe_words = set(recipe_ing_str.split())
        match_count = sum(1 for u_word in user_words if u_word in recipe_words)
                
        overlap_ratio = match_count / len(user_words)
        
        combined_score = similarity_scores[i] + (overlap_ratio * 1.5)
        
        if combined_score > best_score:
            best_score = combined_score
            best_index = i

    if best_score <= 0 or best_index == -1:
        return None

    return {
        "Name": df.iloc[best_index]['Title'],
        "Ingredients": df.iloc[best_index]['Ingredients'],
        "Instructions": df.iloc[best_index]['Instructions']
    }

def top_n_recipes(user_input, n=5):
    """
    ML Vector Retrieval Function:
    Transforms user token sets into ML vectors to fetch the top `n` ranking recipe candidates 
    sorted systematically by their algorithmic fitness score.
    """
    if not user_input or user_input.strip() == "":
        return []

    user_input_clean = preprocess_text(user_input)
    if not user_input_clean:
        return []
        
    user_words = set(user_input_clean.split())
    if not user_words:
        return []
        
    user_vec = vectorizer.transform([user_input_clean])
    similarity_scores = cosine_similarity(user_vec, tfidf_matrix).flatten()
    
    scored_indices = []
    
    for i, row in df.iterrows():
        recipe_ing_str = row['clean_ingredients']
        if not recipe_ing_str:
            continue
            
        recipe_words = set(recipe_ing_str.split())
        match_count = sum(1 for u_word in user_words if u_word in recipe_words)
        overlap_ratio = match_count / len(user_words)
        
        combined_score = similarity_scores[i] + (overlap_ratio * 1.5)
        if combined_score > 0:
            scored_indices.append((i, combined_score))

    scored_indices.sort(key=lambda x: x[1], reverse=True)
    
    final_indices = [pt[0] for idx, pt in enumerate(scored_indices) if idx < n]

    recommendations = []
    for idx in final_indices:
        recommendations.append({
            "Name": df.iloc[idx]['Title'],
            "Ingredients": df.iloc[idx]['Ingredients'],
            "Instructions": df.iloc[idx]['Instructions']
        })

    return recommendations
