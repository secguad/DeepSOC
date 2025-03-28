from datetime import datetime
from app import db

class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    source = db.Column(db.String(100))
    severity = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Keyword(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AIConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    api_key = db.Column(db.String(200), nullable=False)
    model_name = db.Column(db.String(100))
    max_tokens = db.Column(db.Integer, default=1000)
    temperature = db.Column(db.Float, default=0.7)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AlertConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(50), nullable=False)  # feishu, dingtalk, wecom
    webhook_url = db.Column(db.String(500), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TelegramConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.String(100), nullable=False)
    channel_name = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow) 