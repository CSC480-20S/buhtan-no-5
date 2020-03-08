from flask import Blueprint
from endpoints import Deliver
from endpoints import Purchase

deliver_bp = Blueprint(Deliver,__name__)
purchase_bp= Blueprint(Purchase,__name__)
