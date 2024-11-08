from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import pymysql
import random

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='@Nielong080848',
    database='Hangman_db',
    port=3306
)

app = Flask(__name__)

# ตั้งค่าเชื่อมต่อกับฐานข้อมูล MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%40Nielong080848@localhost:3306/Hangman_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SECRETE KEY
app.config['SECRET_KEY'] = "my super secret key sugoi"

# Initialize The Database
db = SQLAlchemy(app)

# สร้างตารางคำถาม
class Quest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quest = db.Column(db.String(255), nullable=False)
    ans = db.Column(db.String(255), nullable=False)

    def __init__(self, quest, ans):
        self.quest = quest
        self.ans = ans
        
# สร้างตารางชื่อและคะแนน
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    score = db.Column(db.Integer)

    def __init__(self, name, score):
        self.name = name
        self.score = score

# สร้างตารางในฐานข้อมูล
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/infor')
def infor():
    # ดึงข้อมูลผู้ใช้ล่าสุด
    latest_user = User.query.order_by(User.id.desc()).first()
    
    if latest_user:
        username = latest_user.name
        score = latest_user.score

        # คำนวณลำดับ
        leaderboard = User.query.order_by(User.score.desc()).all()
        rank = next((i + 1 for i, user in enumerate(leaderboard) if user.id == latest_user.id), "N/A")
    else:
        username, score, rank = "ไม่มีข้อมูล", 0, "N/A"

    return render_template('information.html', username=username, score=score, rank=rank)

@app.route('/leader')
def leader():
    top_users = User.query.order_by(User.score.desc()).limit(10).all()
    return render_template('leaderboard.html', users=top_users)

@app.route('/fail')
def fail():
    score = request.args.get('score')
    return render_template('fail.html', score=score)

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

@app.route('/play', methods=['GET', 'POST'])
def play():
    # ดึงคำถามทั้งหมดจากฐานข้อมูล
    all_qnas = Quest.query.all()

    # ตรวจสอบว่ามีคำถามในฐานข้อมูลหรือไม่
    if len(all_qnas) >= 5:
        # เลือกคำถาม 5 คำถามแบบสุ่มจากคำถามทั้งหมด
        random_qnas = random.sample(all_qnas, 5)
    else:
        # ถ้าจำนวนคำถามในฐานข้อมูลมีน้อยกว่า 5 ข้อ ให้แสดงคำถามทั้งหมดที่มี
        random_qnas = all_qnas

    return render_template('play.html', qnas=random_qnas)

@app.route('/save_user_score', methods=['POST'])
def save_user_score():
    username = request.form.get('username')
    score = request.form.get('score', type=int)  # แก้ไขให้รับค่า score ที่เป็น integer
    
    if score is None:  # ตรวจสอบว่าค่า score ที่ส่งมาถูกต้อง
        score = 0
    
    # บันทึกชื่อและคะแนนในฐานข้อมูล
    user = User(name=username, score=score)
    db.session.add(user)
    db.session.commit()
    
    return redirect(url_for('infor'))  # เปลี่ยนเส้นทางไปหน้า Information.html หลังบันทึกข้อมูล

if __name__ == '__main__':
    app.run(debug=True)
