from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from datetime import timedelta
from backend.listing import listing_post, listing_get
from backend.register import register_user
from backend.login import user_login
from backend.snippet import get_snippet, create_snippett, get_snippets_with_more_likes
from backend.user import get_user

app = Flask(__name__)
app.config["SECRET_KEY"] = "super-secret-key"
app.config["JWT_SECRET_KEY"] = "jwt-secret-key"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)


app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_ACCESS_COOKIE_NAME"] = "access_token"
app.config["JWT_COOKIE_CSRF_PROTECT"] = False

jwt = JWTManager(app)

@jwt.unauthorized_loader
def unauthorized_callback(callback):
    # Quando o token não existe
    return redirect(url_for('login'))

@jwt.invalid_token_loader
def invalid_token_callback(error):
    # Quando o token é inválido (ex: corrompido)
    return redirect(url_for('login'))

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    # Quando o token expirou
    response = redirect(url_for('login'))
    response.delete_cookie("access_token")  # remove o cookie antigo
    return response

@app.route('/')
@jwt_required(optional=True)
def home():
    user = get_jwt_identity()
    user_dict = get_user(user)
    snippets = get_snippets_with_more_likes()
    return render_template("./home.html", user=user_dict["name"], snippets=snippets)


@app.route('/listing', methods=["GET", "POST"])
@jwt_required(optional=True)
def listing():
    user = get_jwt_identity()
    user_dict = get_user(user)
    if not user:
        return redirect(url_for('login'))

    # valores padrão
    search = None
    filter_language = None

    if request.method == "POST":
        search = request.form.get("search", "").strip()
        filter_language = request.form.get("filter", "").strip()

    # Lógica principal
    if search or filter_language:
        snippets = listing_post(search, filter_language)
    else:
        snippets = listing_get()

    return render_template("listing.html", user=user_dict["name"], snippets=snippets)



@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        response = user_login(email, password)
        if response:
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

@app.route('/register', methods=["GET", "POST"])
@app.route('/register')
def register():
    if request.method == "POST":
        email = request.form.get("email")
        name = request.form.get("name")
        password = request.form.get("password")

        response = register_user(email, name, password)
        if response:
            access_token = create_access_token(identity=email)
            response = make_response(redirect(url_for("home")))
            
            
            response.set_cookie("access_token", access_token, httponly=True)
            return response
        else:
            return render_template("./register-form.html", error="esse email já está cadastrado")



    return render_template("./register-form.html")


@app.route('/snippet')
@jwt_required(optional=True)
def snippet():
    user = get_jwt_identity()
    user_dict = get_user(user)
    if not user:
        return redirect(url_for('login'))
    

    snippet_id = request.args.get("id", type=int)
    if not snippet_id:
        return "ID do snippet não informado", 400

    snippet_data = get_snippet(snippet_id)
    if not snippet_data:
        return "Snippet não encontrado", 404

    return render_template(
        "snippet.html",
        user=user_dict["name"],
        snippet=snippet_data
    )


@app.route('/create_snippet', methods=["GET", "POST"])
@jwt_required(optional=True)
def create_snippet():
    user = get_jwt_identity()
    print(user)
    if not user:
        return redirect(url_for('login'))
    user_dict = get_user(user)
    
    if request.method == "POST":
        
        snippet = {
            "title" : request.form.get("title"),
            "language" : request.form.get("language"),
            "description" : request.form.get("description"),
            "version" : request.form.get("version"),
            "code" : request.form.get("code-input"),
            "output" : request.form.get("output-input")
        }

        response = create_snippett(snippet, user_dict)
        if response:
            response = make_response(redirect(url_for("home")))
            return response
        else:
            return render_template("./snippet-form.html", error="algo deu errado")
    
    return render_template("./snippet-form.html", user=user_dict["name"])


if __name__ == "__main__":
    app.run(debug=True)
