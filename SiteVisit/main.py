import sqlite3
from flask import Flask, render_template, g, abort, make_response, url_for, session
from adminPanel.admin import admin
from authorize.login import user
from useful.FDataBase import FDataBase


app = Flask(__name__)
app.config["SECRET_KEY"] = "wewrtrtey1223345dfgdf"
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'uploads'

app.register_blueprint(user, url_prefix="/user")
app.register_blueprint(admin, url_prefix="/admin")

dbase = None
file_profile = [
    {'html': 'profile.html', 'css': 'css/pro_style.css'},
    {'html': 'profile1.html', 'css': 'css/pro_style1.css'},
    {'html': 'profile2.html', 'css': 'css/pro_style2.css'},
]


@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = FDataBase(db)


def connect_db():
    conn = sqlite3.connect('site_visit_DB.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_db():
    if not hasattr(g, "link_db"):
        g.link_db = connect_db()
    return g.link_db


def create_db():
    db = connect_db()
    with app.open_resource("sql_db.sql", mode="r") as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


@app.route('/userava')
def userava():
    img = get_avatar()
    if not img:
        return ""
    answer = make_response(img)
    answer.headers["Content-Type"] = "image/png"
    return answer


def get_avatar():
    img = None
    if not session["avatar"]:
        try:
            with app.open_resource(app.root_path + url_for('static', filename='img/profile-image.jpg'), "rb") as file:
                img = file.read()
        except FileNotFoundError as e:
            print(f"Дефолтный аватар не найден. {e}")
    else:
        try:
            with app.open_resource(app.root_path + "/uploads/" + session["avatar"], "rb") as file:
                img = file.read()
        except FileNotFoundError as e:
            print(f"Файл аватара не найден. {e}")
            try:
                with app.open_resource(app.root_path + url_for('static', filename='img/profile-image.jpg'),
                                       "rb") as file:
                    img = file.read()
                    print(f"Успешно использован дефолтный аватар.")
            except FileNotFoundError as e:
                print(f"Дефолтный аватар не найден. {e}")
    return img


@app.route("/")
def index():
    (session['firstname'], session['lastname'], session['email'], session['phone'],
     session['profession'], session['about'], session['social'], session['avatar'],
     session['type_profile']) = ("Ethan", "Rivers", "evan@google.com", 79009007777, "UI / UX Designer",
                                 "Lorem ipsum dolor sit amet consectetur adipisicing elit. Magnum atque, ipsam a amet "
                                 "laboriosam eligendi.", [{"name": "dribbble", "url": "https://dribbble.com/"},
                                                          {"name": "instagram", "url": "https"
                                                                                       "://instagram.com/"},
                                                          {"name": "twitter", "url": "https"
                                                                                     "://x.com/"},
                                                          {"name": "linkedin",
                                                           "url": "https://careers"
                                                                  ".linkedin.cn/"},
                                                          {"name": "facebook",
                                                           "url": "https://facebook.com/"},
                                                          {"name": "behance",
                                                           "url": "https://www.behance.net/"}],
                                 False, 2)
    return render_template(file_profile[session['type_profile']]['html'],
                           css_file=file_profile[session['type_profile']]['css'], title="Main")


@app.route("/<alias>", methods=["GET", "POST"])
def showpost(alias):
    (session['user_name'], session['firstname'], session['lastname'], session['email'],
     session['phone'], session['profession'], session['about'], session['social'],
     session['avatar'], session['type_profile']) = dbase.get_profile(alias)

    print(f"showpost - {session}")

    if not session['user_name']:
        abort(404)

    return render_template(file_profile[session['type_profile']]['html'],
                           css_file=file_profile[session['type_profile']]['css'], title=alias)


@app.errorhandler(404)
def pageNotFounded(error):
    return render_template("page404.html", title="Страница не найдена")


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "link_db"):
        g.link_db.close()


if __name__ == "__main__":
    create_db()
    app.run(debug=True)
