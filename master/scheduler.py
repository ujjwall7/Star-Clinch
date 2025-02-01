from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import datetime
from django.core.mail import send_mail

import boto3
import csv
from io import StringIO
from django.conf import settings
from master.models import User  


def send_daily_email():
    print('send_daily_email')
    today = datetime.datetime.today().weekday()  # 0=Monday, 6=Sunday
    if today in [5, 6]:  # Saturday (5) or Sunday (6)
        return  # Weekend me kuch mat bhejo

    subject = "Daily Update"
    message = "Yeh ek daily scheduled email hai."
    recipient_list = ["sharmaujjwal0921@gmail.com"]  
    
    send_mail(subject, message, "ujjwal@gftpl.com", recipient_list)
    print("Email Sent Successfully!")


def upload_user_data_to_s3():
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )

    # Specify the bucket name
    bucket_name = 'your-bucket-name'

    # Create a CSV buffer
    csv_buffer = StringIO()
    writer = csv.writer(csv_buffer)
    writer.writerow(['Username', 'Email', 'User Type'])  # Header

    # Fetch user data from the database
    for user in User.objects.all():
        writer.writerow([user.username, user.email, user.user_type])

    # Upload the CSV data to S3
    s3_client.put_object(
        Bucket=bucket_name,
        Key='weekly_user_data.csv',
        Body=csv_buffer.getvalue()
    )

    print("User data uploaded to S3 successfully!")

# Schedule the job weekly
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(upload_user_data_to_s3, CronTrigger(hour=6, minute=0, day_of_week='mon'))
    scheduler.start()

def start():
    scheduler1 = BackgroundScheduler()
    scheduler1.add_job(send_daily_email, "cron", hour=6, minute=0, replace_existing=True, max_instances=1)
    scheduler1.start()









