from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from datetime import timedelta

app = Flask(__name__)
app.config["SECRET_KEY"] = "super-secret-key"
app.config["JWT_SECRET_KEY"] = "jwt-secret-key"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)


app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_ACCESS_COOKIE_NAME"] = "access_token"
app.config["JWT_COOKIE_CSRF_PROTECT"] = False

jwt = JWTManager(app)

USERS = {
    "teste@teste.com": "123456",
}


@app.route('/')
@jwt_required(optional=True)
def home():
    user = get_jwt_identity()
    return render_template("./home.html", user=user)


@app.route('/listing')
@jwt_required(optional=True)
def listing():
    user = get_jwt_identity()
    if not user:
        return redirect(url_for('login'))
    return render_template("./listing.html", user=user)


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if email in USERS and USERS[email] == password:
            access_token = create_access_token(identity=email)
            response = make_response(redirect(url_for("home")))
            
            
            response.set_cookie("access_token", access_token, httponly=True)
            return response
        else:
            return render_template("./login-form.html", error="Credenciais inválidas")

    return render_template("./login-form.html")


@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('login')))
    response.delete_cookie("access_token")
    return response


@app.route('/register')
def register():
    return render_template("./register-form.html")


@app.route('/snippet')
@jwt_required(optional=True)
def snippet():
    user = get_jwt_identity()
    if not user:
        return redirect(url_for('login'))
    return render_template("./snippet.html", user=user)


@app.route('/create_snippet')
@jwt_required(optional=True)
def create_snippet():
    user = get_jwt_identity()
    if not user:
        return redirect(url_for('login'))
    return render_template("./snippet-form.html", user=user)


if __name__ == "__main__":
    app.run(debug=True)
