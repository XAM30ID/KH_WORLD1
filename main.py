from flask import Flask, render_template, url_for,request, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///person.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Persons(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String, nullable=False)
    name_lastname = db.Column(db.String, nullable=False)
    about = db.Column(db.Text, nullable=False)
    vk_link = db.Column(db.String, nullable=False)
    inst_link = db.Column(db.String, nullable=False)
    secret = db.Column(db.String, default="None")
    photo = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
def index():
    persons = Persons.query.order_by(Persons.id).all()
    return render_template("index.html", persons=persons)


@app.route('/person-adding', methods=['POST', 'GET'])
def person_adding():
    if request.method == 'POST':
        nickname = request.form['nickname']
        name_lastname = request.form['name_lastname']
        about = request.form['about']
        vk_link = request.form['vk_link']
        inst_link = request.form['inst_link']
        secret = request.form['secret']

        photo = request.files.getlist('photo')
        if not os.path.exists(f"static/images/{request.form['name_lastname']}"):
            os.mkdir(f"static/images/{request.form['name_lastname']}")
        path = f"static/images/{request.form['name_lastname']}/"
        for elem in photo:
            elem.save(os.path.join(path, elem.filename))

        person = Persons(nickname=nickname, name_lastname=name_lastname, about=about, vk_link=vk_link,
                         inst_link=inst_link, secret=secret, photo=path)

        try:
            db.session.add(person)
            db.session.commit()
            return redirect('/')
        except:
            return 'Ошибка'

    else:
        return render_template("person_adding.html")

if __name__ == "__main__":
    app.run(debug=True)