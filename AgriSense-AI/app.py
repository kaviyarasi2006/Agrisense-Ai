from flask import Flask, render_template, request, redirect, url_for
from database.db import db
from models.llm_handler import get_crop_solution
from utils.validator import validate_input

app = Flask(__name__)

collection = db["farmer_queries"]
users = db["users"]   # 🔐 NEW collection for login/signup


# =======================
# Home Page
# =======================
@app.route("/")
def home():
    return render_template("index.html")

# =======================
# SIGNUP PAGE
# =======================
@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        users.insert_one({
            "name": name,
            "email": email,
            "password": password
        })

        return redirect(url_for("login"))
    return render_template("signup.html")


# =======================
# LOGIN PAGE
# =======================
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        user = users.find_one({"email": email, "password": password})

        if user:
           return redirect(url_for("home"))
        else:
            return "Invalid Credentials"

    return render_template("login.html")


# =======================
# Analyze Page
# =======================
@app.route("/analyze")
def analyze():
    return render_template("analyze.html")


# =======================
# Submit Form
# =======================
@app.route("/submit", methods=["POST"])
def submit():

    farmer_name = request.form.get("farmerName", "").strip()
    crop_name = request.form.get("cropName", "").strip()
    problem = request.form.get("problemDescription", "").strip()
    language = request.form.get("language", "English")

    is_valid, msg = validate_input(problem)

    if not is_valid:
        return render_template(
            "result.html",
            farmer_name=farmer_name,
            crop_name=crop_name,
            problem=problem,
            solution=msg
        )

    ai_response = get_crop_solution(crop_name, problem, language)

    data = {
        "farmer_name": farmer_name,
        "crop_name": crop_name,
        "problem": problem,
        "language": language,
        "solution": ai_response
    }

    try:
        collection.insert_one(data)
        print("✅ Data saved successfully")
    except Exception as e:
        print("❌ MongoDB Error:", e)

    return render_template(
        "result.html",
        farmer_name=farmer_name,
        crop_name=crop_name,
        problem=problem,
        solution=ai_response
    )


# =======================
# DASHBOARD PAGE
# =======================
@app.route("/dashboard")
def dashboard():

    total_queries = collection.count_documents({})

    pipeline = [
        {"$group": {"_id": "$crop_name", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 1}
    ]

    result = list(collection.aggregate(pipeline))
    most_crop = result[0]["_id"] if result else "No Data"

    total_languages = len(collection.distinct("language"))
    recent_queries = collection.find().sort("_id", -1).limit(5)

    return render_template(
        "dashboard.html",
        total_queries=total_queries,
        most_crop=most_crop,
        total_languages=total_languages,
        recent_queries=recent_queries
    )


# =======================
# HISTORY PAGE
# =======================
@app.route("/history")
def history():
    data = collection.find().sort("_id", -1)
    return render_template("history.html", data=data)


# =======================
# RUN APP
# =======================
if __name__ == "__main__":
    app.run()