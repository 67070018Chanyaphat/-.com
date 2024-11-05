from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import pymysql

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='@Nielong080848',
    database='hangman_db',
    port=3306
)

app = Flask(__name__)

# ตั้งค่าเชื่อมต่อกับฐานข้อมูล MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%40Nielong080848@localhost:3306/hangman_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SECRETE KEY
app.config['SECRET_KEY'] = "my super secret key sugoi"

# Initialize The Database
db = SQLAlchemy(app)

# สร้างโมเดลข้อมูล
class Quest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quest = db.Column(db.String(255), nullable=False)
    ans = db.Column(db.String(255), nullable=False)

    def __init__(self, quest, ans):
        self.quest = quest
        self.ans = ans

# สร้างตารางในฐานข้อมูล
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/infor')
def infor():
    return render_template('information.html')

@app.route('/leader')
def leader():
    return render_template('leaderboard.html')

@app.route('/fail')
def fail():
    return render_template('fail.html')

@app.route('/add_qna', methods=['GET', 'POST'])
def handle_qna():
    if request.method == 'POST':
        quest = request.form['quest']
        ans = request.form['ans']
        print(quest, ans)  # ตรวจสอบว่าข้อมูลถูกส่งมาหรือไม่

        # เพิ่มข้อมูลลงฐานข้อมูล
        new_qna = Quest(quest=quest, ans=ans)
        db.session.add(new_qna)
        db.session.commit()

        return redirect(url_for('index'))
    else:
        # ดึงข้อมูลทั้งหมดจากฐานข้อมูล
        all_qna = Quest.query.all()
        return render_template('test.html', qnas=all_qna)

@app.route('/play')
def play():
    # ดึงคำถามทั้งหมดจากฐานข้อมูล
    all_qnas = Quest.query.all()
    return render_template('play.html', qnas=all_qnas)

if __name__ == '__main__':
    app.run(debug=True)
