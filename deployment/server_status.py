import subprocess,os
from flask_restful import Resource
from flask import jsonify
from endpoints import Auxiliary
class Status(Resource):
    @Auxiliary.auth_dec
    def get(self):
        process = subprocess.Popen(['git', 'log' ,'-1'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            stdout, stderr = process.communicate(timeout=20)  # believe this is blocking
            return jsonify({"version":stdout.decode('UTF-8')})
        except subprocess.TimeoutExpired as e:
            process.kill()
            return jsonify({"msg":str(e)})




