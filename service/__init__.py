"""
服务层
"""


from service.user_serivce import UserService
from service.auth_service import AuthService
from service.task_service import task_service

user_service = UserService()
auth_service = AuthService()

__all__ = ['auth_service', 'user_service', 'task_service']