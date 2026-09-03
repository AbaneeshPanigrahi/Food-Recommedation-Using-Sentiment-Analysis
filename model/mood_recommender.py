"""
Machine Learning (ML) and Natural Language Processing (NLP) Mood Recommender.
Applies NLP text preprocessing and rule-based ML scoring algorithms (Jaccard-like intersection similarity) 
to classify raw emotional sentiment strings into structured culinary prediction vectors.
"""

import pandas as pd
import re
import nltk
import os
from nltk.corpus import stopwords

try:
    stop_words = set(stopwords.words("english"))
except LookupError:
    nltk.download("stopwords")
    stop_words = set(stopwords.words("english"))

DATA_PATH = "datasets/mood_food_recommender.csv"

if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

df = pd.read_csv(DATA_PATH)

if 'Mood' not in df.columns or 'Food' not in df.columns:
    if 'mood' in df.columns and 'food' in df.columns:
        df = df.rename(columns={'mood': 'Mood', 'food': 'Food'})
    else:
        raise ValueError("CSV columns do not match required columns: 'Mood' and 'Food'")

df = df[['Mood', 'Food']].dropna().reset_index(drop=True)

def preprocess_text(text):
    """
    NLP Tokenization and Normalization Pipeline:
    Parses row data down to core alphanumeric English tokens via regex stripping 
    and dictionary-based stopword elimination to improve ML signal-to-noise ratio.
    """
    text = str(text).lower()
    text = re.sub(r'[^a-z\s]', '', text)
    tokens = text.split()
    tokens = [t for t in tokens if t not in stop_words]
    return " ".join(tokens)

df['clean_mood'] = df['Mood'].apply(preprocess_text)

def recommend_food(user_input, top_n=3):
    """
    ML Rule-Based Predictive Model:
    Generates algorithmic textual similarities to fetch the top N dietary mappings.
    Utilizes weighted NLP intersection overlaps as a heuristic fallback for dataset gaps.
    """
    if not user_input or user_input.strip() == "":
        return "Please enter your mood."

    user_input_clean = preprocess_text(user_input)
    if not user_input_clean:
        return "No clear mood detected."

    exact_matches = df[df['clean_mood'] == user_input_clean]
    if not exact_matches.empty:
        foods = exact_matches['Food'].unique().tolist()
        return ", ".join(foods[:top_n])

    user_words = set(user_input_clean.split())
    scores = []
    
    for _, row in df.iterrows():
        mood_words = set(row['clean_mood'].split())
        if not mood_words:
            continue
            
        intersection = user_words.intersection(mood_words)
        base_score = len(intersection)
        
        if base_score > 0:
            if len(intersection) == len(mood_words):
                base_score += 5
                
            scores.append((base_score, row['Food']))

    scores.sort(reverse=True, key=lambda x: x[0])

    if scores:
        results = []
        seen = set()
        for score, food in scores:
            if food not in seen:
                results.append(food)
                seen.add(food)
            if len(results) == top_n:
                break
        return ", ".join(results)

    return "No food found for this mood."

def list_all_moods():
    """
    Returns an index list of unique mapped target moods for dropdown consumption.
    """
    return df['Mood'].unique().tolist()



