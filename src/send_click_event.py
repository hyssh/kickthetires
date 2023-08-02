# send a click event to Event Hubs
import os
import json
import dotenv
from azure.eventhub import EventHubProducerClient, EventData
from user_profile import User_profile
from cars import Car

class ClickEvent:
    dotenv.load_dotenv()

    # Create a producer client to send messages to the event hub.

    def __init__(self, user_profile, car):
        self.producer = EventHubProducerClient.from_connection_string(os.environ["EVENT_HUB_CONNECTION_STRING"])
        self.user_profile = user_profile
        self.car = car

    def send(self):
        # send a single message
        payload_dict = {'user_profile': [self.user_profile.to_json()], 'car': [self.car.to_json()]}
        print(json.dumps(payload_dict))
        event_data_batch = self.producer.create_batch()
        event_data_batch.add(EventData(json.dumps(payload_dict)))
        self.producer.send_batch(event_data_batch)
        # Close the producer.
        self.producer.close()

    def __str__(self):
        return f"{self.user_profile} clicked on {self.car}"
