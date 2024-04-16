import json
from django.conf import settings
from booking.models import booking
from pymongo import MongoClient
from datetime import datetime

# Function to convert Excel serial date to Python datetime
def excel_to_datetime(excel_date_num):
    return datetime.fromordinal(datetime(1900, 1, 1).toordinal() + int(excel_date_num) - 2)

def run():
    """
    Imports data from a JSON file into the booking model, routing to even or odd based on guest_id.
    """
    booking.objects.using('even').delete()
    booking.objects.using('odd').delete()
    with open("hotel_bookings.json", 'r') as file:
        data = json.load(file)['Sheet1'] 

        for item in data[:30]:
            guest_id = item['guest_id']
            
            database = 'even' if int(guest_id) % 2 == 0 else 'odd'

            booking.objects.using(database).filter(guest_id=guest_id).delete()
            
            booking_record = {
                'guest_id': guest_id,
                'full_name': item['full_name'],
                'room_number': item.get('room_number', None),
                'room_type': item.get('room_type', None),
                'check_in_date': excel_to_datetime(item['check_in_date']),
                'check_out_date': excel_to_datetime(item['check_out_date']),
                'price_per_night': item.get('price_per_night', None),
                'total_cost': item.get('total_cost', None),
            }

            # Create a new booking record in the designated database
            booking = booking.objects.using(database).create(**booking_record)
            print(f'Added booking for guest {booking.full_name} to database {database}')

# Note: Ensure the 'booking' model and the JSON file's keys match exactly with the model fields.
