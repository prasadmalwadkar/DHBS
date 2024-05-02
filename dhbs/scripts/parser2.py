import json
from django.conf import settings
from booking.models import booking
from pymongo import MongoClient
from datetime import datetime, timedelta

# Function to convert Excel serial date to Python datetime
def json_to_datetime(excel_date_num):
    return datetime.fromordinal(datetime(1900, 1, 1).toordinal() + int(excel_date_num) - 2)

# def json_to_datetime(json_date):
#     try:
#         dt = datetime.strptime(json_date, "%m/%d/%y")
#         return dt.strftime("%B %d, %Y")
#     except ValueError:
#         return None

def run():
    """
    Imports data from a JSON file into the booking model, routing to even or odd based on guest_id.
    """
    booking.objects.using('even').delete()
    booking.objects.using('odd').delete()
    with open("Complete_Booking_Dataset.json", 'r') as file:
        data = json.load(file)['Sheet1'] 

        for item in data:
            guest_id = item['guest_id']
            
            database = 'even' if int(guest_id) % 2 == 0 else 'odd'

          
            
            booking_record = {
                'booking_id': item['booking_id'],
                'guest_id': item['guest_id'],
                'full_name': item['full_name'],
                'room_number': item.get('room_number', None),
                'room_type': item.get('room_type', None),
                'check_in_date': json_to_datetime(item['check_in_date']),
                'check_out_date': json_to_datetime(item['check_out_date']),
                'price_per_night': item.get('price_per_night', None),
                'total_cost': item.get('total_cost', None),
            }

            # Create a new booking record in the designated database
            new_booking = booking.objects.using(database).create(**booking_record)
            print(f'Added booking for guest {new_booking.full_name} to database {database}')

