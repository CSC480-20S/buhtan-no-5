from flask import jsonify

def handle_auth(e):
    return jsonify(error=str(e)),401


