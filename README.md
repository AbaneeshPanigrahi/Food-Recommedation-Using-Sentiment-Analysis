<div align="center">

# 🍽️ Mood-Based Food Recommender

**Personalized food discovery powered by mood and ingredient-based recommendations.**

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Web%20App-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

</div>

---

## Overview

A Flask web application that helps users discover food based on their mood or the ingredients they have. It includes account registration and login, recipe recommendations, mood-based suggestions, and a food recommendation chatbot.

## Features

- **Ingredient-based recipes** — find recipe suggestions using ingredients you enter.
- **Mood-based food suggestions** — explore food recommendations that match your mood.
- **Recommendation chatbot** — ask for help discovering food.
- **User accounts** — register, log in, and access personalized app pages.
- **Feedback form** — send feedback through the contact page.

## Tech stack

- **Backend:** Python, Flask
- **Recommendation/data processing:** pandas, scikit-learn, NLTK
- **Database:** SQLite
- **Frontend:** HTML templates and static assets

## Getting started

### Requirements

- Python 3.9 or newer
- Git

### Installation

```bash
git clone https://github.com/AbaneeshPanigrahi/Food-Recommedation-Using-Sentiment-Analysis.git
cd Food-Recommedation-Using-Sentiment-Analysis

python -m venv .venv
```

Activate the virtual environment:

```bash
# macOS / Linux
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Install dependencies and start the app:

```bash
python -m pip install -r requirements.txt
python app.py
```

Then open **http://127.0.0.1:5000** in your browser. Create an account to access the recommendation features.

## Project structure

```text
├── app.py                 # Flask routes and application entry point
├── model/                 # Recommendation and chatbot logic
├── templates/             # HTML pages
├── static/                # Frontend assets
├── recipes.csv            # Recipe data
├── mood_food_recommender.csv
├── requirements.txt       # Python dependencies
└── LICENSE
```

## Configuration and security

This project is intended for local development. Before deploying it publicly, move the Flask secret key into an environment variable, disable Flask debug mode, and review database and account security settings. Never commit production credentials or user data to the repository.

## Contributing

Bug reports and improvements are welcome. Open an issue to discuss a significant change before submitting a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

Built by [Abaneesh Panigrahi](https://github.com/AbaneeshPanigrahi)

</div>
