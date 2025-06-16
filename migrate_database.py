#!/usr/bin/env python3
"""
数据库迁移脚本
用于删除现有表并重新创建新的表结构
注意：此操作会删除所有现有数据！
"""

import sys
from mysql_client import create_tables, drop_tables, get_db_session, UserModel
from util.logging import logger

def backup_users():
    """备份现有用户数据"""
    try:
        with get_db_session() as db:
            users = db.query(UserModel).all()
            backup_data = []
            for user in users:
                backup_data.append({
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'password': user.password,
                    'status': user.status,
                    'created_at': user.created_at
                })
            return backup_data
    except Exception as e:
        logger.warning(f"Failed to backup users (table might not exist): {e}")
        return []

def migrate_database():
    """执行数据库迁移"""
    try:
        logger.info("开始数据库迁移...")
        
        # 1. 尝试备份现有数据
        logger.info("正在备份现有用户数据...")
        backup_data = backup_users()
        logger.info(f"备份了 {len(backup_data)} 个用户")
        
        # 2. 删除现有表
        logger.info("正在删除现有表...")
        drop_tables()
        logger.info("现有表已删除")
        
        # 3. 创建新表结构
        logger.info("正在创建新表结构...")
        create_tables()
        logger.info("新表结构已创建")
        
        # 4. 恢复用户数据（仅基础字段）
        if backup_data:
            logger.info("正在恢复用户数据...")
            with get_db_session() as db:
                for user_data in backup_data:
                    new_user = UserModel(
                        username=user_data['username'],
                        email=user_data['email'],
                        password=user_data['password'],
                        status=user_data['status'],
                        created_at=user_data['created_at'],
                        # 新字段使用默认值
                        full_name=None,
                        avatar=None,
                        personal_tags=None,
                        long_term_goals=None,
                        recent_focus=None,
                        daily_plan_time="08:00",
                        daily_review_time="22:00",
                        timezone="Asia/Shanghai"
                    )
                    db.add(new_user)
                db.commit()
            logger.info(f"恢复了 {len(backup_data)} 个用户")
        
        logger.info("数据库迁移完成！")
        return True
        
    except Exception as e:
        logger.error(f"数据库迁移失败: {e}")
        return False

def confirm_migration():
    """确认迁移操作"""
    print("⚠️  警告：此操作将删除所有现有数据库表并重新创建！")
    print("📋 操作内容：")
    print("   1. 备份现有用户数据")
    print("   2. 删除所有现有表")
    print("   3. 创建新的表结构")
    print("   4. 恢复用户基础数据")
    print()
    
    while True:
        confirm = input("是否继续？请输入 'yes' 确认，'no' 取消: ").lower().strip()
        if confirm in ['yes', 'y']:
            return True
        elif confirm in ['no', 'n']:
            return False
        else:
            print("请输入 'yes' 或 'no'")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--force":
        # 强制执行，不需要确认
        success = migrate_database()
    else:
        # 需要用户确认
        if confirm_migration():
            success = migrate_database()
        else:
            print("迁移已取消")
            success = False
    
    if success:
        print("✅ 数据库迁移成功完成！")
        print("现在可以重新启动服务并测试注册功能")
        sys.exit(0)
    else:
        print("❌ 数据库迁移失败")
        sys.exit(1) 