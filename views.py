from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3


app = Flask(__name__)
app.secret_key = "secret_key"

def get_posts():
    conn = sqlite3.connect("posts.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM posts ORDER BY datetime DESC")
    posts = cur.fetchall()
    conn.close()
    return posts

def get_post(post_id):
    conn = sqlite3.connect("posts.db")
    cur = conn.cursos()
    cur.execute("SELECT * FROM posts WHERE id=?", (post_id,))
    post = cur.fetchone()
    conn.close()
    return post
  
@app.route("/post/<int:post_id>")
def post(post_id):
    post = get_post(post_id)
    return render_template("post.html", post=post)
    


@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        password_hash = generate_password_hash(password)
        
        session["username"] = username
        
        return redirect(url_for("index"))
    return render_template("signup.html")
 
@app.before_request
def before_request():
    if "username" not in session and request.endpoint != "login":
        return redirect(url_for("login"))
 
@app.route("/")
def index():
    posts = get_posts()
    return render_template("index.html", posts=posts, username=session.get("username"))

 
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        user = user.query.filter.by(email=email).first()
        
        if user and check_password_hash(user.password.hash, password):
            session["username"] = user.username
            return redirect(url_for("index"))
        else:
          error = "Incorrect email or password"
          
    return render_template("login.html", error=error)
  
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))
  
if __name__ == "__main__":
    app.run(debug=True)