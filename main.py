from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # SQLite for simplicity
db = SQLAlchemy(app)
with app.app_context():
    db.create_all()

class Button(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_clicked = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

@app.route("/")
def index():
    with open("index.html", 'r', encoding="utf-8") as f:
        raw = f.read()
        f.close()
    return raw

@app.route('/button-clicked', methods=['POST'])
def button_clicked():
    button = Button.query.first()
    if not button:
        button = Button()
        db.session.add(button)
    button.last_clicked = datetime.utcnow()
    db.session.commit()
    return jsonify({'message': 'Button clicked successfully'})

def send_email():
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login("dailybuttonchecker@gmail.com", "hpmlnkciavuhxxlh")
        msg = MIMEText("The button was not clicked today!")
        msg['From'] = "dailybuttonchecker@gmail.com"
        msg['To'] = "jean.heibig@orange.fr"
        msg['Subject'] = "Button Alert"
        server.sendmail("dailybuttonchecker@gmail.com", "jean.heibig@orange.fr", msg.as_string())

def check_button_status():
    button = Button.query.first()
    if not button or button.last_clicked < datetime.utcnow() - timedelta(minutes=5):
        send_email()

if __name__ == "__main__":
    app.run(debug=True)
