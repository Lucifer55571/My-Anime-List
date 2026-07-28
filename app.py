import os

import requests

from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    flash,
    request
)

from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from config import Config
from models import db, User, Anime

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

#Buat Login

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message = "Silakan login terlebih dahulu."
login_manager.login_message_category = "warning"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#Home Page

@app.route("/")
def index():
    total_users = User.query.count()
    total_anime = Anime.query.count()

    try:
        response = requests.get("https://api.jikan.moe/v4/top/anime", timeout=10)
        response.raise_for_status()
        top_anime = response.json().get("data", [])[:6]
    except requests.RequestException:
        top_anime = []

    return render_template(
        "index.html",
        total_users=total_users,
        total_anime=total_anime,
        top_anime=top_anime
    )


@app.route("/api/jikan")
def jikan_api():
    query = request.args.get("q", "")
    try:
        if query:
            response = requests.get(
                "https://api.jikan.moe/v4/anime",
                params={"q": query},
                timeout=10
            )
        else:
            response = requests.get("https://api.jikan.moe/v4/top/anime", timeout=10)

        response.raise_for_status()
        data = response.json().get("data", [])
        return {"success": True, "data": data}
    except requests.RequestException as exc:
        return {"success": False, "error": str(exc)}, 500

#Register

@app.route("/register", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm = request.form.get("confirm_password")

        if password != confirm:
            flash("Konfirmasi password tidak sama.", "danger")
            return redirect(url_for("register"))

        user_username = User.query.filter_by(username=username).first()

        if user_username:
            flash("Username sudah digunakan.", "danger")
            return redirect(url_for("register"))

        user_email = User.query.filter_by(email=email).first()

        if user_email:
            flash("Email sudah digunakan.", "danger")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)

        user = User(
            username=username,
            email=email,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        flash("Registrasi berhasil.", "success")

        return redirect(url_for("login"))

    return render_template("register.html")

#Login

@app.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):

            login_user(user)

            flash("Login berhasil.", "success")

            return redirect(url_for("dashboard"))

        flash("Username atau password salah.", "danger")

    return render_template("login.html")

#Logout

@app.route("/logout")
@login_required
def logout():

    logout_user()

    flash("Berhasil logout.", "info")

    return redirect(url_for("index"))

#Dashboard

@app.route("/dashboard")
@login_required
def dashboard():

    anime = Anime.query.filter_by(user_id=current_user.id).all()

    total = len(anime)

    watching = Anime.query.filter_by(
        user_id=current_user.id,
        status="Watching"
    ).count()

    completed = Anime.query.filter_by(
        user_id=current_user.id,
        status="Completed"
    ).count()

    on_hold = Anime.query.filter_by(
        user_id=current_user.id,
        status="On Hold"
    ).count()

    dropped = Anime.query.filter_by(
        user_id=current_user.id,
        status="Dropped"
    ).count()

    plan = Anime.query.filter_by(
        user_id=current_user.id,
        status="Plan to Watch"
    ).count()

    return render_template(
        "dashboard.html",
        total=total,
        watching=watching,
        completed=completed,
        on_hold=on_hold,
        dropped=dropped,
        plan=plan
    )

#YourAnimeList

@app.route("/anime")
@login_required
def anime_list():

    keyword = request.args.get("search", "")

    if keyword:
        anime = Anime.query.filter(
            Anime.user_id == current_user.id,
            Anime.title.ilike(f"%{keyword}%")
        ).all()
    else:
        anime = Anime.query.filter_by(
            user_id=current_user.id
        ).all()

    return render_template(
        "anime_list.html",
        anime_list=anime
    )

#Detail

@app.route("/anime/<int:id>")
@login_required
def detail(id):

    anime = Anime.query.filter_by(
        id=id,
        user_id=current_user.id
    ).first_or_404()

    return render_template(
        "detail.html",
        anime=anime
    )

#Create

@app.route("/anime/add", methods=["GET", "POST"])
@login_required
def add_anime():

    if request.method == "POST":

        anime = Anime(
            title=request.form["title"],
            genre=request.form["genre"],
            studio=request.form["studio"],
            episodes=request.form["episodes"],
            status=request.form["status"],
            score=request.form["score"],
            release_year=request.form["release_year"],
            cover_url=request.form["cover_url"],
            synopsis=request.form["synopsis"],
            user_id=current_user.id
        )

        db.session.add(anime)
        db.session.commit()

        flash("Anime berhasil ditambahkan.", "success")

        return redirect(url_for("anime_list"))

    return render_template("add_anime.html")

#Update

@app.route("/anime/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_anime(id):

    anime = Anime.query.filter_by(
        id=id,
        user_id=current_user.id
    ).first_or_404()

    if request.method == "POST":

        anime.title = request.form["title"]
        anime.genre = request.form["genre"]
        anime.studio = request.form["studio"]
        anime.episodes = request.form["episodes"]
        anime.status = request.form["status"]
        anime.score = request.form["score"]
        anime.release_year = request.form["release_year"]
        anime.cover_url = request.form["cover_url"]
        anime.synopsis = request.form["synopsis"]

        db.session.commit()

        flash("Anime berhasil diperbarui.", "success")

        return redirect(url_for("anime_list"))

    return render_template(
        "edit_anime.html",
        anime=anime
    )

#Delete

@app.route("/anime/delete/<int:id>")
@login_required
def delete_anime(id):

    anime = Anime.query.filter_by(
        id=id,
        user_id=current_user.id
    ).first_or_404()

    db.session.delete(anime)
    db.session.commit()

    flash("Anime berhasil dihapus.", "success")

    return redirect(url_for("anime_list"))

#Profile

@app.route("/profile")
@login_required
def profile():

    total = Anime.query.filter_by(
        user_id=current_user.id
    ).count()

    return render_template(
        "profile.html",
        total=total
    )

#Error

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_server(error):
    return render_template("500.html"), 500

#Main

with app.app_context():
    try:
        db.create_all()
    except Exception as exc:
        print(f"Database initialization warning: {exc}")


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=app.config.get("DEBUG", False)
    )