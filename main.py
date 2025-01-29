from flask import Flask, render_template, request, jsonify,request, redirect, url_for
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import google.generativeai as genai
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import firebase_admin
from firebase_admin import credentials, db
import datetime



# Your Firebase Admin SDK credentials JSON file path (download from Firebase console)
cred = credentials.Certificate("firebasedatabase.json")  # Replace with your file path
firebase_admin.initialize_app(cred, {
    'databaseURL': "#Firebase Databse URL"  # Replace with your database URL
})

db = db.reference()  # Get a database reference

app = Flask(__name__)

# Set your Gemini API key
genai.configure(api_key="#GEMINI API KEY")

# Sample text data (replace with your actual text loading from file)
text_file_path = "amazon-faq.txt"  # Replace with the actual path
try:
    with open(text_file_path, 'r', encoding='utf-8') as file:
        text_data = file.read()
except FileNotFoundError:
    text_data = "Sample text data. Replace with your file content." #Fallback


# Vectorize the text data (FIT AND TRANSFORM the text_data)
vectorizer = TfidfVectorizer()
text_vectors = vectorizer.fit_transform([text_data])

def post_log(query, response):
    """
    Posts two variables and a timestamp to Firebase, using the query as the ID.
    """


    now = str(datetime.datetime.now())
    data = {
        "timestamp": now,
        "query": query,
        "response": response
    }

    # Use the timestamp string as the key (ID)
    db.child(query).set(data) # Replace your_firebase_path
    return True



def get_gemini_response(user_query, user_vector):  # Use user_vector
    # Calculate cosine similarity
    similarity_scores = cosine_similarity(user_vector, text_vectors)
    most_similar_index = np.argmax(similarity_scores)
    context = text_data.split(".")[most_similar_index]

    prompt = f"""
    You are the expert FAQ Assistant for Amazon EC2, your task is to answer the user queries,
    Answer the question in as detailed manner as possible from the provided context, make sure to provide all the details, if the answer is not in the provided
    context then just say, "answer is not available in the context, visit https://aws.amazon.com/ec2/faqs/", dont provide the wrong answer. Dont give too huge answers, so user's can't feel it's too much big answers.\n\n
    
    Context: {context}\n
    User: {user_query}\nGemini:
    """

    try:

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        return response.text
    except Exception as e:
        return f"Error in Gemini API: {e}"

@app.route("/chatwithtxt")
def chatwithtxt():
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_query = request.form["user_input"]
    user_vector = vectorizer.transform([user_query])  # Vectorize user query
    gemini_response = get_gemini_response(user_query, user_vector)  # Pass user_vector

    post=post_log(user_query, gemini_response)
    if post==True:

        return jsonify({"response": gemini_response})

#route for user login
@app.route('/user_login')
def user_login():

    return render_template('user_dashboard.html') # Redirect to user dashboard

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_id = request.form['admin_id']
        admin_password = request.form['admin_password']

        # Replace with your actual admin authentication logic
        if admin_id == 'admin' and admin_password == 'password':  # Example credentials
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin_login.html', error='Invalid credentials')
    return render_template('admin_login.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')


@app.route('/edit_logs', methods=["GET", "POST"])  # Route for Edit Log button
def edit_file():
    encoding = 'utf-8'
    TEXT_FILE = "amazon-faq.txt"  # File to edit
    if request.method == "POST":
        content = request.form["content"]
        with open(TEXT_FILE, "w", encoding=encoding) as file:
            file.write(content)

    if os.path.exists(TEXT_FILE):
        with open(TEXT_FILE, "r", encoding=encoding) as file:
            content = file.read()
    else:
        content = ""

    return render_template("editor.html", content=content)

def get_all_data():
    try:
        data = db.get()

        if isinstance(data, dict):  # If it's already a Python dictionary
            retrieved_data = data  # Use it directly
        else:  # If it's a Firebase snapshot
            retrieved_data = data.val()  # Use .val() to get the data
        return retrieved_data

    except Exception as e:
        return {"error": str(e)}

@app.route('/view_log')  # Route for View Log button
def showdata():
    data = get_all_data()
    return render_template("getdata.html", data=data)

# Routes for login and main page
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)  # Set debug=False in production
