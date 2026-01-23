from flask import Blueprint, jsonify
from backend.models import User

bp = Blueprint('admin', __name__)

@bp.route("/users", methods=["GET"])
def users():
    return jsonify([u.to_dict() for u in User.query.all()])
