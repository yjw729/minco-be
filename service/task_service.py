from typing import Optional, List
from datetime import datetime
from sqlalchemy import and_, or_, desc, asc
from sqlalchemy.orm import Session
import uuid

from models import TaskDto, TaskCreateDto, TaskUpdateDto, TaskListResponseDto
from mysql_client import get_db_session, TaskModel
from util.logging import logger


class TaskService:
    """任务服务类"""

    def convert_task_model_to_dto(self, task_model: TaskModel) -> TaskDto:
        """将数据库模型转换为DTO"""
        try:
            return TaskDto(
                id=task_model.id,
                title=task_model.title,
                description=task_model.description,
                emoji=task_model.emoji,
                category_id=task_model.category_id,
                project_id=task_model.project_id,
                start_time=task_model.start_time.isoformat() + "Z" if task_model.start_time else None,
                end_time=task_model.end_time.isoformat() + "Z" if task_model.end_time else None,
                estimated_duration=task_model.estimated_duration,
                time_slot_id=task_model.time_slot_id,
                priority=task_model.priority,
                status_id=task_model.status_id,
                is_overdue=task_model.is_overdue or False,
                sub_tasks=task_model.sub_tasks or [],
                created_at=task_model.created_at.isoformat() + "Z",
                updated_at=task_model.updated_at.isoformat() + "Z",
                completed_at=task_model.completed_at.isoformat() + "Z" if task_model.completed_at else None
            )
        except Exception as e:
            logger.error(f"任务模型转换失败: {str(e)}")
            raise e

    async def get_tasks(
        self,
        user_id: int,
        date: Optional[str] = None,
        project_id: Optional[str] = None,
        category_id: Optional[int] = None,
        status_id: Optional[int] = None,
        priority: Optional[int] = None,
        is_completed: Optional[bool] = None,
        time_slot_id: Optional[int] = None,
        sort_by: str = "created_at",
        order: str = "desc",
        page: int = 1,
        limit: int = 20
    ) -> TaskListResponseDto:
        """获取用户的任务列表"""
        try:
            logger.info(f"开始获取用户任务列表 - 用户ID: {user_id}, 页码: {page}, 每页: {limit}")

            with get_db_session() as db:
                # 构建查询条件
                query = db.query(TaskModel).filter(TaskModel.user_id == user_id)

                # 应用筛选条件
                if category_id:
                    query = query.filter(TaskModel.category_id == category_id)
                
                if status_id:
                    query = query.filter(TaskModel.status_id == status_id)
                
                if priority:
                    query = query.filter(TaskModel.priority == priority)
                
                if project_id:
                    query = query.filter(TaskModel.project_id == project_id)
                
                if time_slot_id:
                    query = query.filter(TaskModel.time_slot_id == time_slot_id)
                
                if is_completed is not None:
                    if is_completed:
                        query = query.filter(TaskModel.completed_at.isnot(None))
                    else:
                        query = query.filter(TaskModel.completed_at.is_(None))
                
                # 日期筛选
                if date:
                    try:
                        filter_date = datetime.strptime(date, "%Y-%m-%d").date()
                        query = query.filter(
                            or_(
                                TaskModel.start_time >= filter_date,
                                TaskModel.end_time >= filter_date,
                                and_(
                                    TaskModel.start_time.is_(None),
                                    TaskModel.end_time.is_(None)
                                )
                            )
                        )
                    except ValueError:
                        logger.warning(f"无效的日期格式: {date}")

                # 排序
                if hasattr(TaskModel, sort_by):
                    if order.lower() == "desc":
                        query = query.order_by(desc(getattr(TaskModel, sort_by)))
                    else:
                        query = query.order_by(asc(getattr(TaskModel, sort_by)))
                else:
                    # 默认按创建时间倒序
                    query = query.order_by(desc(TaskModel.created_at))

                # 获取总数
                total_items = query.count()
                
                # 分页
                offset = (page - 1) * limit
                tasks = query.offset(offset).limit(limit).all()

                # 转换为DTO
                task_dtos = [self.convert_task_model_to_dto(task) for task in tasks]

                # 构建分页信息
                total_pages = (total_items + limit - 1) // limit
                pagination = {
                    "total_items": total_items,
                    "total_pages": total_pages,
                    "current_page": page,
                    "limit": limit,
                    "has_next": page < total_pages,
                    "has_prev": page > 1
                }

                logger.info(f"成功获取用户任务列表 - 用户ID: {user_id}, 返回: {len(task_dtos)} 个任务, 总数: {total_items}")

                return TaskListResponseDto(
                    items=task_dtos,
                    pagination=pagination
                )

        except Exception as e:
            logger.error(f"获取用户任务列表失败 - 用户ID: {user_id}, 错误: {str(e)}")
            raise e

    async def create_task(self, user_id: int, task_data: TaskCreateDto) -> TaskDto:
        """创建新任务"""
        try:
            logger.info(f"开始创建任务 - 用户ID: {user_id}, 标题: {task_data.title}")

            with get_db_session() as db:
                # 生成UUID
                task_id = str(uuid.uuid4())
                
                # 处理时间字段
                start_time = None
                end_time = None
                if task_data.start_time:
                    try:
                        start_time = datetime.fromisoformat(task_data.start_time.replace('Z', '+00:00'))
                    except ValueError:
                        logger.warning(f"无效的开始时间格式: {task_data.start_time}")
                
                if task_data.end_time:
                    try:
                        end_time = datetime.fromisoformat(task_data.end_time.replace('Z', '+00:00'))
                    except ValueError:
                        logger.warning(f"无效的结束时间格式: {task_data.end_time}")

                # 创建任务模型
                new_task = TaskModel(
                    id=task_id,
                    user_id=user_id,
                    title=task_data.title,
                    description=task_data.description,
                    emoji=task_data.emoji,
                    category_id=task_data.category_id,
                    project_id=task_data.project_id,
                    start_time=start_time,
                    end_time=end_time,
                    estimated_duration=task_data.estimated_duration,
                    time_slot_id=task_data.time_slot_id,
                    priority=task_data.priority,
                    status_id=task_data.status_id or 1,
                    sub_tasks=task_data.sub_tasks or [],
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )

                db.add(new_task)
                db.commit()
                db.refresh(new_task)

                logger.info(f"任务创建成功 - 任务ID: {task_id}, 用户ID: {user_id}")

                return self.convert_task_model_to_dto(new_task)

        except Exception as e:
            logger.error(f"创建任务失败 - 用户ID: {user_id}, 错误: {str(e)}")
            raise e

    async def get_task_by_id(self, user_id: int, task_id: str) -> Optional[TaskDto]:
        """根据ID获取单个任务"""
        try:
            logger.info(f"获取任务详情 - 用户ID: {user_id}, 任务ID: {task_id}")

            with get_db_session() as db:
                task = db.query(TaskModel).filter(
                    and_(TaskModel.id == task_id, TaskModel.user_id == user_id)
                ).first()

                if not task:
                    logger.warning(f"任务不存在 - 用户ID: {user_id}, 任务ID: {task_id}")
                    return None

                logger.info(f"成功获取任务详情 - 任务ID: {task_id}")
                return self.convert_task_model_to_dto(task)

        except Exception as e:
            logger.error(f"获取任务详情失败 - 用户ID: {user_id}, 任务ID: {task_id}, 错误: {str(e)}")
            raise e


# 创建全局实例
task_service = TaskService() 