import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from src.models.quiz import db
from src.routes.quiz import quiz_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'photography-quiz-secret-key-2024'

app.register_blueprint(quiz_bp)

# Database configuration
# 使用絕對路徑確保部署環境能正確找到數據庫
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database', 'app.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 確保數據庫目錄存在
db_dir = os.path.dirname(db_path)
if not os.path.exists(db_dir):
    os.makedirs(db_dir)

db.init_app(app)
with app.app_context():
    db.create_all()
    
    # 初始化默認推薦設定
    from src.models.quiz import RecommendationSettings
    try:
        existing_default = RecommendationSettings.query.filter_by(setting_name='default').first()
        if not existing_default:
            default_setting = RecommendationSettings(
                setting_name='default',
                min_courses=3,
                max_courses=8,
                is_active=True,
                description='系統默認推薦設定，推薦3-8個課程'
            )
            db.session.add(default_setting)
            db.session.commit()
            print("✅ 默認推薦設定創建成功")
        else:
            # 如果沒有啟用的設定，啟用默認設定
            active_settings = RecommendationSettings.query.filter_by(is_active=True).all()
            if not active_settings:
                existing_default.is_active = True
                db.session.commit()
                print("✅ 已啟用默認推薦設定")
    except Exception as e:
        print(f"⚠️ 初始化推薦設定時出現問題: {str(e)}")
        db.session.rollback()

# 公開版本路由 - 只有問卷功能
@app.route('/public')
def public_quiz():
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404
    
    public_path = os.path.join(static_folder_path, 'public.html')
    if os.path.exists(public_path):
        return send_from_directory(static_folder_path, 'public.html')
    else:
        return "public.html not found", 404

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

