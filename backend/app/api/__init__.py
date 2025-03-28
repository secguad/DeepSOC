from flask import Blueprint

bp = Blueprint('api', __name__)

from app.api import (
    dashboard,
    alerts,
    keywords,
    ai_config,
    alert_config,
    telegram_config
) 