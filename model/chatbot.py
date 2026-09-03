"""
Natural Language Processing (NLP) and Machine Learning (ML) Chatbot Engine.
This module acts as the AI conversational interface, utilizing NLP tokenization 
and heuristic-based ML classification to analyze unstructured user text, extract intent/sentiment, 
and dynamically map semantic inputs to food and recipe recommendation models.
"""

import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
import os
import sys


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from model.recipe_recommender import recommend_recipe
from model.mood_recommender import recommend_food

try:
    stop_words = set(stopwords.words('english'))
except LookupError:
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))

DATA_PATH = "datasets/mood_food_recommender.csv"
if os.path.exists(DATA_PATH) and os.path.getsize(DATA_PATH) > 0:
    df = pd.read_csv(DATA_PATH)
    if 'Mood' not in df.columns and 'mood' in df.columns:
        df = df.rename(columns={'mood': 'Mood'})
else:
    df = pd.DataFrame([{"Mood": "happy", "Food": "pizza"}])

if 'Mood' not in df.columns:
    df['Mood'] = "happy"
if 'Food' not in df.columns:
    df['Food'] = "pizza"

df['clean_mood'] = df['Mood'].apply(lambda x: re.sub(r'[^a-z\s]', '', str(x).lower()))

def preprocess_text(text):
    """
    NLP Preprocessing Pipeline:
    Sanitizes raw chatbot strings by applying lowercase normalization, regex-based 
    noise reduction, and NLTK stopword extraction to isolate high-value tokens.
    """
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    return ' '.join([w for w in text.split() if w not in stop_words])

def detect_mood(text):
    """
    ML/NLP Sentiment Predictor:
    Parses user input via NLP to find the strongest matching emotional state classifier 
    using weighted word intersections, returning the top predictive ML food outputs.
    """
    text = preprocess_text(text)
    user_words = set(text.split())
    
    if not user_words:
        return "I couldn't understand your mood."

    exact_matches = df[df['clean_mood'] == text]
    if not exact_matches.empty:
        return exact_matches.iloc[0]['Food']

    scores = []
    
    for _, row in df.iterrows():
        mood_words = set(row['clean_mood'].split())
        if not mood_words:
            continue
            
        intersection = user_words.intersection(mood_words)
        base_score = len(intersection)
        
        if base_score > 0:
            if len(mood_words) > 1 and len(intersection) == len(mood_words):
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
            if len(results) == 3:
                break
        return ", ".join(results)
    
    return "I couldn't understand your mood."

def chatbot_reply(message, last_recommended_food=None):
    """
    Main entry point for chatbot interactions, returning formatted response strings and context state.
    """

    message_lower = message.lower()
    
    if "hello" in message_lower or "hi " in message_lower or message_lower.strip() == "hi":
        return "Hello! I am your AI Food Assistant. Tell me your mood, or give me some ingredients to find a recipe!", last_recommended_food
        
    recipe_keywords = ["recipe", "ingredients", "cook", "make", "have", "share"]
    
    recipe_keywords = ["recipe", "ingredients", "cook", "make", "have", "share"]

    if any(keyword in message_lower for keyword in recipe_keywords):
        
        search_query = message_lower
        is_follow_up = False
        
        if "the recipe" in message_lower or "that recipe" in message_lower or "share" in message_lower:
            if last_recommended_food:
                search_query = last_recommended_food
                is_follow_up = True
                
        recipe_result = recommend_recipe(search_query)
        if recipe_result:
            prefix = "Here is the recipe for that!" if is_follow_up else "I found a great recipe for you!"
            return f"{prefix} 🧑‍🍳 <strong>{recipe_result['Name']}</strong><br><small><strong>Ingredients:</strong> {recipe_result['Ingredients']}</small><br><br><strong>Instructions:</strong><br><small>{recipe_result['Instructions']}</small>", last_recommended_food
            
    mood_food = detect_mood(message)
    if mood_food != "I couldn't understand your mood.":
        first_food = mood_food.split(",")[0].strip()
        return f"Based on your mood, I recommend: <strong>{mood_food}</strong>", first_food
        
    return "I couldn't understand your request. Try saying 'I am happy' or 'Find a recipe with chicken'.", last_recommended_food
