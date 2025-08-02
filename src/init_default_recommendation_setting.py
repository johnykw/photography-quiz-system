#!/usr/bin/env python3
"""
初始化默認推薦設定
"""

import sys
import os

# 添加當前目錄到Python路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# 導入應用和模型
from main import app
from models.quiz import db, RecommendationSettings

def init_default_recommendation_setting():
    """初始化默認推薦設定"""
    with app.app_context():
        try:
            # 檢查是否已存在默認設定
            existing_default = RecommendationSettings.query.filter_by(setting_name='default').first()
            
            if not existing_default:
                # 創建默認設定
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
                print(f"   設定名稱: {default_setting.setting_name}")
                print(f"   課程數量範圍: {default_setting.min_courses}-{default_setting.max_courses}")
                print(f"   狀態: {'啟用' if default_setting.is_active else '停用'}")
            else:
                print("ℹ️  默認推薦設定已存在")
                print(f"   設定名稱: {existing_default.setting_name}")
                print(f"   課程數量範圍: {existing_default.min_courses}-{existing_default.max_courses}")
                print(f"   狀態: {'啟用' if existing_default.is_active else '停用'}")
                
                # 如果沒有啟用的設定，啟用默認設定
                active_settings = RecommendationSettings.query.filter_by(is_active=True).all()
                if not active_settings:
                    existing_default.is_active = True
                    db.session.commit()
                    print("✅ 已啟用默認推薦設定")
                    
        except Exception as e:
            print(f"❌ 初始化默認推薦設定失敗: {str(e)}")
            db.session.rollback()

if __name__ == '__main__':
    init_default_recommendation_setting()

