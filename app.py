from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///submissions.db'
db = SQLAlchemy(app)

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Submission {self.name}>'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    email = request.form.get('email')
    new_submission = Submission(name=name, email=email)
    db.session.add(new_submission)
    db.session.commit()
    return redirect(url_for('result', name=name, email=email))

@app.route('/result')
def result():
    name = request.args.get('name')
    email = request.args.get('email')
    return render_template('result.html', name=name, email=email)

@app.route('/submissions')
def submissions():
    all_submissions = Submission.query.all()
    return render_template('submissions.html', submissions=all_submissions)

if __name__ == '__main__':
    with app.app_context():
      db.create_all()
    app.run(debug=True)
