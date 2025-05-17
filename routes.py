from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import requests
from sqlalchemy import create_engine

from db_connection import create_url
from db_crud import read_user_request_type


##############################
# common used variable
##############################

FORWARD_BASE_URL = "http://localhost:5002"

url = create_url(ordinal = 1, database_product = "postgresql")
engine = create_engine(url)

forward_bp = Blueprint("forward", __name__)


##############################
# routing function
##############################

@forward_bp.route("/<path:path>", methods = ["POST", "GET", "PUT", "PATCH", "DELETE"])
@jwt_required()
def forward(path):
    try:
        identity = get_jwt_identity()
        method = request.method
        request_permission = read_user_request_type(connection_engine = engine, username = identity, request_method = method)
        print(request_permission)
        if request_permission is None:
            return jsonify({"msg": "Permission denied"}), 401
        target_url = f"{FORWARD_BASE_URL}/{path}"
        headers = dict(request.headers)
        headers.pop("Host", None) # hilangkan header Host supaya nanti diganti dengan host tempat tujuan saat sampai
        resp = requests.request(
            method = method,
            url = target_url,
            params = request.args.to_dict(),
            headers = headers, # kirim informasi client ke backend untuk autentikasi berbasis JWT (RBAC, logging)
            data = request.get_data() # data dari client yang ingin diproses
        )
        return (resp.content, resp.status_code, resp.headers.items())
    except Exception as e:
        return jsonify({"error": str(e)}), 500
