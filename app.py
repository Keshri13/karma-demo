from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///karma.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Karma(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow )

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
    
@app.route("/", methods = ['GET','POST'])
def hello_world():
    if request.method=='POST':
        title = request.form['inputTitle']
        desc = request.form['inputDesc']
        karma = Karma(title = title, desc = desc)
        db.session.add(karma)
        db.session.commit()
    allKarma = Karma.query.all()
    return render_template('index.html', allKarma = allKarma)

@app.route("/show")
def show_karma():
    allKarma = Karma.query.all()
    print(allKarma)
    return "Hello, Keshu1! "

@app.route("/delete/<int:sno>")
def delete(sno):
    karma = Karma.query.filter_by(sno=sno).first()
    db.session.delete(karma)
    db.session.commit()
    return redirect("/")

@app.route("/update/<int:sno>", methods = ['GET','POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['inputTitle']
        desc = request.form['inputDesc']
        karma = Karma.query.filter_by(sno=sno).first()
        karma.title = title
        karma.desc = desc
        db.session.add(karma)
        db.session.commit()
        return redirect("/")

    karma = Karma.query.filter_by(sno=sno).first()
    return render_template('update.html',karma=karma)

@app.route("/keshu")
def hello_keshu():
    return "Hello, Keshu1! "

@app.route("/demo")
def demo():
    # return "Hello, World!*2"
    return render_template('demo2.html')

if __name__ == "__main__":
    app.run(debug=True, port=8080)