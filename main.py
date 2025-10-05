from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("./home.html")


@app.route('/listing')
def listing():
    return render_template("./listing.html")

@app.route('/login')
def login():
    return render_template("./login-form.html")

@app.route('/register')
def register():
    return render_template("./register-form.html")

@app.route('/snippet')
def snippet():
    return render_template("./snippet.html")

@app.route('/create_snippet')
def create_snippet():
    return render_template("./snippet-form.html")



if __name__ == "__main__":
    app.run(debug=True)