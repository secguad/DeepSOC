from flask import Blueprint
from app.api.v1 import keywords, monitor, robot

api_router = Blueprint("api", __name__)

# 注册子路由
api_router.register_blueprint(keywords.router)
api_router.register_blueprint(monitor.router)
api_router.register_blueprint(robot.router) 