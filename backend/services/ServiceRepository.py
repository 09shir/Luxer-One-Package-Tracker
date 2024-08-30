from repository.DeliveryRepository import get_all_deliveries, create_delivery, get_delivery_by_id, update_delivery, delete_delivery
from functions.emails import get_new_luxer_one_email
from datetime import datetime, timedelta

def get_all_deliverys_service():
    return get_all_deliveries()

def get_delivery_by_id_service(delivery_id):
    return get_delivery_by_id(delivery_id)

def create_delivery_service(access_code, days, date):
    return create_delivery(access_code, days, date)

def update_delivery_service(delivery_id, access_code, days, date):
    update_delivery(delivery_id, access_code, days, date)

def delete_delivery_service(delivery_id):
    delete_delivery(delivery_id)

def batch_job_service():
    print('running')
    email_details = get_new_luxer_one_email()
    past_deliveries = get_all_deliverys_service()

    if email_details is not None:
        for email_detail in email_details:
            if email_detail['days'] != 0:
                old_delivery = [d for d in past_deliveries if d.access_code == email_detail['access_code']]
                if old_delivery:
                    delete_delivery_service(old_delivery[0].id) 

    # clears remaining ones
    for past_delivery in past_deliveries:
        past_delivery.days += 1
        if past_delivery.days == 1 or past_delivery.days >= 7:
            delete_delivery_service(past_delivery.id) 
        elif past_delivery.days == 2:
            delete_delivery_service(past_delivery.id)
        elif past_delivery.days == 4:
            delete_delivery_service(past_delivery.id)
    if email_details is not None:
        for email_detail in email_details:
            date2 = datetime.strptime(email_detail['date'], "%Y-%m-%d %H:%M:%S %Z")
            date2 = date2 - timedelta(days=email_detail['days'])
            date2 = date2.strftime("%Y-%m-%d %H:%M:%S %Z")
            create_delivery_service(email_detail['access_code'], email_detail['days'], date2)
    else:
        print("no new delivery notice today")
    