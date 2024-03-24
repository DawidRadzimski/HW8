import pika
import json
from mongoengine import connect
from models import Contact
from connect import connect_to_mongodb

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
print("Connection successful.")
channel = connection.channel()
channel.queue_declare(queue='email_queue')

connect_to_mongodb()

def send_email(contact):
    print(f"Sending email to {contact.full_name} at {contact.email}...")
    contact.sent_email = True
    contact.save()
    print(f"Email sent to {contact.full_name} at {contact.email}")

def callback(ch, method, properties, body):
    message = json.loads(body)
    contact_id = message['contact_id']
    contact = Contact.objects.get(id=contact_id)
    send_email(contact)

channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
