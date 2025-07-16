from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from app.crud import crud_keyword
from app.schemas.keyword import KeywordCreate, KeywordUpdate
from app.db.session import get_db

router = Blueprint("keywords", __name__)

@router.route("/keywords", methods=["GET"])
def get_keywords():
    try:
        db = next(get_db())
        word = request.args.get("word")
        category = request.args.get("category")
        is_active = request.args.get("is_active")
        skip = int(request.args.get("skip", 0))
        limit = int(request.args.get("limit", 100))
        
        keywords = crud_keyword.get_keywords(
            db, 
            word=word, 
            category=category, 
            is_active=is_active,
            skip=skip, 
            limit=limit
        )
        return jsonify({
            "code": 1,
            "message": "获取关键词列表成功",
            "data": keywords
        })
    except Exception as e:
        return jsonify({
            "code": 0,
            "message": f"获取关键词列表失败: {str(e)}"
        }), 500

@router.route("/keywords", methods=["POST"])
def create_keyword():
    try:
        db = next(get_db())
        data = request.get_json()
        keyword_in = KeywordCreate(**data)
        
        # 检查关键词是否已存在
        db_keyword = crud_keyword.get_keyword_by_word(db, word=keyword_in.word)
        if db_keyword:
            return jsonify({
                "code": 0,
                "message": "关键词已存在"
            }), 400
            
        keyword = crud_keyword.create_keyword(db, obj_in=keyword_in)
        return jsonify({
            "code": 1,
            "message": "创建关键词成功",
            "data": keyword.id
        })
    except Exception as e:
        return jsonify({
            "code": 0,
            "message": f"创建关键词失败: {str(e)}"
        }), 500

@router.route("/keywords/<int:keyword_id>", methods=["PUT"])
def update_keyword(keyword_id: int):
    try:
        db = next(get_db())
        data = request.get_json()
        keyword_in = KeywordUpdate(**data)
        
        keyword = crud_keyword.update_keyword(db, db_obj_id=keyword_id, obj_in=keyword_in)
        return jsonify({
            "code": 1,
            "message": "更新关键词成功",
            "data": keyword
        })
    except Exception as e:
        return jsonify({
            "code": 0,
            "message": f"更新关键词失败: {str(e)}"
        }), 500

@router.route("/keywords/<int:keyword_id>", methods=["DELETE"])
def delete_keyword(keyword_id: int):
    try:
        db = next(get_db())
        crud_keyword.delete_keyword(db, db_obj_id=keyword_id)
        return jsonify({
            "code": 1,
            "message": "删除关键词成功"
        })
    except Exception as e:
        return jsonify({
            "code": 0,
            "message": f"删除关键词失败: {str(e)}"
        }), 500 