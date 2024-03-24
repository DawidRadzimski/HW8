import pika
import json
from faker import Faker
from mongoengine import connect
from models import Contact
from connect import connect_to_mongodb

fake = Faker()

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
print("Connection successful.")
channel = connection.channel()
channel.queue_declare(queue='email_queue')

connect_to_mongodb()

def generate_fake_contacts(num_contacts):
    for _ in range(num_contacts):
        contact = Contact(
            full_name=fake.name(),
            email=fake.email(),
            sent_email=False  # Initially set to False
            # Add other fields as needed
        )
        contact.save()
        message = {'contact_id': str(contact.id)}
        channel.basic_publish(exchange='', routing_key='email_queue', body=json.dumps(message))
        print(f" [x] Sent {message}")

if __name__ == '__main__':
    num_contacts_to_generate = 10
    generate_fake_contacts(num_contacts_to_generate)
