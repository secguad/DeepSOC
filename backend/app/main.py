from flask import Flask, jsonify
from flask_cors import CORS
from app.core.config import settings
from app.api.v1 import api_router
import logging

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:5184"]}})

# 注册路由
app.register_blueprint(api_router, url_prefix=settings.API_V1_STR)

@app.route("/")
def read_root():
    return jsonify({"message": "Welcome to DeepSOC API"})

@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Error occurred: {str(e)}")
    return jsonify({
        "code": 0,
        "message": str(e)
    }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True) 