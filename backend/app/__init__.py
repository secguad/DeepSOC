# backend/app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from elasticsearch import Elasticsearch
from prometheus_client import CollectorRegistry
from config import Config
from celery import Celery

db = SQLAlchemy()
jwt = JWTManager()
es = Elasticsearch()
registry = CollectorRegistry()

celery = Celery(
    'deepsoc',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1'
)

# 配置Celery
celery.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Shanghai',
    enable_utc=True
)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 初始化扩展
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    
    # 初始化Elasticsearch
    es.init(
        hosts=[app.config['ELASTICSEARCH_URL']],
        basic_auth=(
            app.config['ELASTICSEARCH_USER'],
            app.config['ELASTICSEARCH_PASSWORD']
        )
    )
    
    # 注册蓝图
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # 创建数据库表
    with app.app_context():
        db.create_all()
    
    return app
