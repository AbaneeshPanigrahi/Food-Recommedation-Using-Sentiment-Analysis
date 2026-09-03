from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from functools import wraps
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


from model.recipe_recommender import recommend_recipe, top_n_recipes
from model.mood_recommender import recommend_food, list_all_moods
from model.chatbot import chatbot_reply

app = Flask(__name__)
app.secret_key = "food_recommendation_secret_key"

def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


init_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/home")
@login_required
def home():
    return render_template("home.html")

@app.route("/feedback", methods=["POST"])
def feedback():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()
    
    if name and email and message:
        conn = sqlite3.connect('users.db', timeout=10)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO feedback (name, email, message) VALUES (?, ?, ?)", (name, email, message))
        conn.commit()
        conn.close()
        flash("Thank you for your feedback!", "success")
    else:
        flash("Please fill out all fields in the feedback form.", "danger")
        
    return redirect(url_for('contact'))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        
        conn = sqlite3.connect('users.db', timeout=10)
        cursor = conn.cursor()
        cursor.execute("SELECT id, fullname, password FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['fullname'] = user[1]
            flash("Login successful!", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid email or password", "danger")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('index'))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        fullname = request.form.get("fullname", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        
        hashed_password = generate_password_hash(password)
        
        try:
            conn = sqlite3.connect('users.db', timeout=10)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (fullname, email, password) VALUES (?, ?, ?)", (fullname, email, hashed_password))
            conn.commit()
            conn.close()
            flash("Account created successfully! Please login.", "success")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Email already registered. Try logging in.", "danger")

    return render_template("signup.html")

@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        
        conn = sqlite3.connect('users.db', timeout=10)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()

        # Simple simulation: Always show success to prevent email enumeration
        flash("If your email is registered, a password reset link has been sent.", "success")
        return redirect(url_for('login'))

    return render_template("forgot-password.html")


@app.route("/recipe", methods=["GET", "POST"])
@login_required
def recipe():
    result = None
    recipes = []
    user_ingredients = ""
    error_msg = ""
    
    if request.method == "POST":
        ingredients = request.form.get("ingredients", "").strip()
        if ingredients:
            user_ingredients = ingredients
            result = recommend_recipe(ingredients)
            if result:
                recipes = top_n_recipes(ingredients)
            else:
                error_msg = "No recipes found matching these ingredients."
                
    return render_template("recipe.html", 
                           result=result, 
                           recipes=recipes, 
                           user_ingredients=user_ingredients, 
                           error_msg=error_msg)

@app.route("/mood", methods=["GET", "POST"])
@login_required
def mood():
    """
    Handles the mood-to-food recommendation route.
    Parses the user's emotional state via NLP and renders an aggregated list of matching food items.
    """
    result = ""
    moods = list_all_moods()  # optional: display in dropdown

    if request.method == "POST":
        mood_input = request.form.get("mood", "").strip()
        result = recommend_food(mood_input)
        

        if result and result != "Please enter your mood." and result != "No food found for this mood.":
            return render_template(
                "result.html", 
                mood=mood_input, 
                foods=result.split(", ")
            )

    return render_template("mood.html", result=result, moods=moods)

@app.route("/chatbot", methods=["GET", "POST"])
@login_required
def chatbot():
    if request.method == "POST":
        message = request.form.get("message", "")
        last_food = session.get("last_recommended_food", None)
        reply, new_last_food = chatbot_reply(message, last_food)
        session["last_recommended_food"] = new_last_food
        return jsonify({"reply": reply})
    return render_template("chatbot.html")

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
