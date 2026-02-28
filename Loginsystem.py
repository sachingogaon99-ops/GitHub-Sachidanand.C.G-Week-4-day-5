from flask import Flask, render_template, request, redirect, url_for
import mysql.connector 

app = Flask(__name__)

# Database configuration
DB_CONFIG = {
    'user': 'root',
    'password': 'sachin@686',
    'host': 'localhost',
    'database': 'loginsystem'
}

def get_db_connection():
    """Establishes a database connection."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG) 
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to the database: {err}")
        return None

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if user:
                return redirect(url_for("welcome"))
            else:
                return render_template("login.html", error="Invalid username or password")
        else:
            return render_template("login.html", error="Database connection error")
            
    return render_template("login.html")

@app.route("/welcome")
def welcome():
    return "<h2>welcome<h2>"

if __name__ == "__main__":
    app.run(debug=True)