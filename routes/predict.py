from flask import Blueprint, request, jsonify
from model import predict_career
from utils import token_required

predict_bp = Blueprint("predict", __name__)

@predict_bp.route("/", methods=["POST"])
@token_required
def predict(current_user):
    input_data = request.json

    career, description, links = predict_career(input_data)

    return jsonify({
        "predicted_career": career,
        "job_description": description,
        "related_links": links
    })
