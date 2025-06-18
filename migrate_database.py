#!/usr/bin/env python3
"""
数据库迁移脚本
用于删除现有表并重新创建新的表结构
注意：此操作会删除所有现有数据！
"""

import sys
import os
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mysql_client import create_tables, drop_tables, get_db_session, engine
from sqlalchemy import text
from util.logging import logger

def migrate_database():
    """执行数据库迁移"""
    try:
        logger.info("开始数据库迁移...")
        
        # 创建所有表
        create_tables()
        logger.info("数据库表创建成功")
        
        # 验证表是否创建成功
        with get_db_session() as db:
            # 检查用户表
            result = db.execute(text("SHOW TABLES LIKE 'users'"))
            if result.fetchone():
                logger.info("✅ 用户表 (users) 创建成功")
            else:
                logger.error("❌ 用户表 (users) 创建失败")
                
            # 检查任务表
            result = db.execute(text("SHOW TABLES LIKE 'tasks'"))
            if result.fetchone():
                logger.info("✅ 任务表 (tasks) 创建成功")
                
                # 显示任务表结构
                result = db.execute(text("DESCRIBE tasks"))
                columns = result.fetchall()
                logger.info("任务表结构:")
                for column in columns:
                    logger.info(f"  {column[0]} - {column[1]} - {column[2]} - {column[3]} - {column[4]} - {column[5]}")
            else:
                logger.error("❌ 任务表 (tasks) 创建失败")
        
        logger.info("数据库迁移完成")
        return True
        
    except Exception as e:
        logger.error(f"数据库迁移失败: {str(e)}")
        return False

def reset_database():
    """重置数据库 - 删除所有表并重新创建"""
    try:
        logger.warning("开始重置数据库 (将删除所有数据)...")
        
        # 删除所有表
        drop_tables()
        logger.info("已删除所有表")
        
        # 重新创建表
        return migrate_database()
        
    except Exception as e:
        logger.error(f"数据库重置失败: {str(e)}")
        return False

def check_database_connection():
    """检查数据库连接"""
    try:
        logger.info("检查数据库连接...")
        
        with get_db_session() as db:
            result = db.execute(text("SELECT 1"))
            if result.fetchone():
                logger.info("✅ 数据库连接正常")
                return True
            else:
                logger.error("❌ 数据库连接失败")
                return False
                
    except Exception as e:
        logger.error(f"数据库连接检查失败: {str(e)}")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="数据库迁移工具")
    parser.add_argument("--reset", action="store_true", help="重置数据库 (删除所有表并重新创建)")
    parser.add_argument("--check", action="store_true", help="检查数据库连接")
    
    args = parser.parse_args()
    
    if args.check:
        success = check_database_connection()
    elif args.reset:
        success = reset_database()
    else:
        success = migrate_database()
    
    if success:
        logger.info("操作成功完成")
        sys.exit(0)
    else:
        logger.error("操作失败")
        sys.exit(1) 