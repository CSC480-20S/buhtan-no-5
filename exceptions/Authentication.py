from flask import jsonify

def handle_auth(e):
    print("does this get called?")
    return jsonify(error=str(e)),401


