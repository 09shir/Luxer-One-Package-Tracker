from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from routes.DeliveryRoutes import deliveries_bp
from services.ServiceRepository import batch_job_service
import pytz
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.register_blueprint(deliveries_bp)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

pst_tz = pytz.timezone('America/Los_Angeles')

@app.get("/")
@cross_origin()
def home():
    return "hi"

def start_scheduler():
    scheduler = BackgroundScheduler()
    job = scheduler.add_job(batch_job_service, CronTrigger(hour=21, minute=51, second=25, timezone=pst_tz))
    scheduler.start()
    print("Scheduler started.")
    return scheduler

if __name__ == '__main__':
    # Start the scheduler
    scheduler = start_scheduler()
    app.run(port=5000)