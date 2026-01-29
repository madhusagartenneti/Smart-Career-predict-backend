from flask import Blueprint, request, jsonify
from model import predict_career
from utils import token_required

predict_bp = Blueprint("predict", __name__)

@predict_bp.route("/", methods=["POST"])
@token_required
def predict(current_user):
    data = request.json
    career = predict_career(data)
    return jsonify({"predicted_career": career})
