from flask import Flask, render_template, request, redirect , url_for
from flask_sqlalchemy import SQLAlchemy
import pyshorteners as shr

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Urls(db.Model):
    id_ = db.Column("id_",db.Integer,primary_key = True)
    long = db.Column("long",db.String())
    short = db.Column("short",db.String(3))

    def __init__(self, long, short):
        self.long = long
        self.short = short

def shorten_url(URL):
    try:
        shortener = shr.Shortener()
        shortURL = shortener.tinyurl.short(URL)
        return shortURL
    except Exception as e:
        print(f"Error shortening URL: {e}")
        return None

@app.before_request
def create_tables():
    db.create_all()
@app.route('/', methods = ['POST','GET'])
def home():
    if request.method == "POST":
        url_recieved = request.form["nm"]
        found_url = Urls.query.filter_by(long = url_recieved).first()
        if found_url:
            return f"{found_url.short}"
        else:
            short_url = shorten_url(url_recieved)
            new_url = Urls(url_recieved, short_url)
            db.session.add(new_url)
            db.session.commit()
            return short_url
    else:
        return render_template("home.html")
    
@app.route('/display/<url>')
def display_short_url(url):
    return render_template('shorturl.html',short_url_display = url)

if __name__ == "__main__":
    app.run(debug = True, port = 5000)