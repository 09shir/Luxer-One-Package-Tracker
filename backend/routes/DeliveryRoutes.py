from flask import Blueprint, jsonify, request
from services.ServiceRepository import get_all_deliverys_service, create_delivery_service, get_delivery_by_id_service, update_delivery_service, delete_delivery_service, batch_job_service
from functions.emails import get_new_luxer_one_email
from flask_cors import cross_origin

deliveries_bp = Blueprint('deliveries', __name__)

@deliveries_bp.route('/api/v1/batch_job', methods=['GET'])
@cross_origin()
def batch_job():
    batch_job_service()
    return 'success'


@deliveries_bp.route('/api/v1/deliveries', methods=['GET'])
@cross_origin()
def get_notes():
    deliveries = get_all_deliverys_service()
    deliveries_list = [{'id': delivery.id, 'access_code': delivery.access_code, 'days': delivery.days, 'date': delivery.date} for delivery in deliveries]
    return jsonify({'deliveries': deliveries_list})

@deliveries_bp.route('/api/v1/deliveries/<id>', methods=['DELETE'])
@cross_origin()
def delete_note(id):
    delete_delivery_service(id)
    return jsonify({'deleted': id})