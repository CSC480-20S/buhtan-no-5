import os
from datetime import datetime
from flask import jsonify

path= os.getenv('HOME')+'/csc480/deployment/logs/'

def handle_auth(e):
    return jsonify(error=str(e)), 401

def generic_exception(e):
    '''
    Write the stack trace to file and returns an Internal Server Error 500
    :param e:
    :return:
    '''
    stack_trace = e.orginal_exception
    curr_date = datetime.today().strftime('%Y-%m-%d-%H-%M %Z')
    with open(path+curr_date+".log","w+") as f:
        f.write(str(stack_trace))
        f.write("\n")
    return jsonify(error=str(e)), 500
