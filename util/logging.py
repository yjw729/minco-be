import logging
import sys
import json
from datetime import datetime
from typing import Any, Dict, Optional

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('minco-be.log', encoding='utf-8')
    ]
)

logger = logging.getLogger(__name__)

class APILogger:
    """API专用日志记录器"""
    
    def __init__(self, name: str = "minco-api"):
        self.logger = logging.getLogger(name)
        
    def log_request(self, endpoint: str, method: str, data: Any = None, params: Dict = None, headers: Dict = None, request_id: str = None):
        """记录API请求信息"""
        log_data = {
            "type": "REQUEST",
            "timestamp": datetime.now().isoformat(),
            "request_id": request_id or "unknown",
            "endpoint": endpoint,
            "method": method,
            "params": params,
            "headers": {k: v for k, v in (headers or {}).items() if k.lower() not in ['authorization', 'cookie']},
            "data": self._safe_json_dumps(data)
        }
        self.logger.info(f"🔵 API_REQUEST | {json.dumps(log_data, ensure_ascii=False)}")
        
    def log_response(self, endpoint: str, status_code: int, response_data: Any = None, request_id: str = None, duration_ms: float = None):
        """记录API响应信息"""
        log_data = {
            "type": "RESPONSE", 
            "timestamp": datetime.now().isoformat(),
            "request_id": request_id or "unknown",
            "endpoint": endpoint,
            "status_code": status_code,
            "duration_ms": duration_ms,
            "response": self._safe_json_dumps(response_data)
        }
        
        # 根据状态码选择日志级别
        if status_code >= 500:
            self.logger.error(f"🔴 API_RESPONSE | {json.dumps(log_data, ensure_ascii=False)}")
        elif status_code >= 400:
            self.logger.warning(f"🟡 API_RESPONSE | {json.dumps(log_data, ensure_ascii=False)}")
        else:
            self.logger.info(f"🟢 API_RESPONSE | {json.dumps(log_data, ensure_ascii=False)}")
            
    def log_error(self, endpoint: str, error: Exception, request_id: str = None, extra_data: Dict = None):
        """记录API错误信息"""
        log_data = {
            "type": "ERROR",
            "timestamp": datetime.now().isoformat(),
            "request_id": request_id or "unknown",
            "endpoint": endpoint,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "extra_data": extra_data
        }
        self.logger.error(f"❌ API_ERROR | {json.dumps(log_data, ensure_ascii=False)}")
        
    def log_debug(self, message: str, data: Any = None, request_id: str = None):
        """记录调试信息"""
        log_data = {
            "type": "DEBUG",
            "timestamp": datetime.now().isoformat(),
            "request_id": request_id or "unknown",
            "message": message,
            "data": self._safe_json_dumps(data)
        }
        self.logger.debug(f"🔧 DEBUG | {json.dumps(log_data, ensure_ascii=False)}")
        
    def _safe_json_dumps(self, data: Any) -> Any:
        """安全地序列化数据，处理不可序列化的对象"""
        if data is None:
            return None
        try:
            # 如果是字符串且看起来像密码，则脱敏
            if isinstance(data, dict):
                safe_data = {}
                for k, v in data.items():
                    if isinstance(k, str) and any(keyword in k.lower() for keyword in ['password', 'pwd', 'secret', 'token']):
                        safe_data[k] = "***MASKED***"
                    else:
                        safe_data[k] = v
                return safe_data
            return data
        except Exception:
            return str(data)

# 创建全局API日志记录器实例
api_logger = APILogger()

# 兼容性：保持原有的logger可用
__all__ = ['logger', 'api_logger', 'APILogger'] 