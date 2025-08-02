from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(20), default='single')  # single, multiple
    order = db.Column(db.Integer, nullable=False)
    options = db.Column(db.JSON, nullable=False)  # 存儲選項列表
    correct_answer = db.Column(db.JSON, nullable=True)  # 存儲正確答案
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    level = db.Column(db.String(50), nullable=False)  # beginner, intermediate, advanced
    related_interests = db.Column(db.JSON, nullable=True)  # 相關興趣類型
    is_active = db.Column(db.Boolean, default=True, nullable=False)  # 課程是否開啟
    interest_tags = db.Column(db.JSON, nullable=True)  # 興趣關聯標籤（對應第18題選項）
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ScoreSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level_name = db.Column(db.String(50), nullable=False)  # 等級名稱
    min_score = db.Column(db.Integer, nullable=False)  # 最低分數
    max_score = db.Column(db.Integer, nullable=False)  # 最高分數
    description = db.Column(db.Text, nullable=True)  # 等級描述
    is_active = db.Column(db.Boolean, default=True, nullable=False)  # 是否啟用
    order = db.Column(db.Integer, nullable=False, default=0)  # 排序順序
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    answer = db.Column(db.JSON, nullable=False)  # 存儲用戶答案
    is_correct = db.Column(db.Boolean, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class RecommendationSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    setting_name = db.Column(db.String(100), nullable=False, unique=True)  # 設定名稱
    min_courses = db.Column(db.Integer, nullable=False, default=3)  # 最少推薦課程數量
    max_courses = db.Column(db.Integer, nullable=False, default=8)  # 最多推薦課程數量
    is_active = db.Column(db.Boolean, default=True, nullable=False)  # 是否啟用
    description = db.Column(db.Text, nullable=True)  # 設定描述
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

