# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, request
from django.shortcuts import get_object_or_404
from django.db.models import F
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import booking
from django.db.models import Count, Sum, Avg
from django.contrib import messages
from django.db import DatabaseError



def booking_detail(request, guest_id):
    guest = booking.objects.using('odd' if guest_id % 2 != 0 else 'even').get(guest_id=guest_id)
    return render(request, 'booking/booking_detail.html', {'guest': guest})


def home(request):
    p1 = booking.objects.using('odd').all()
    p2 = booking.objects.using('even').all()

    return render(request, 'booking/home.html', {'guest1': p1, 'guest2': p2})



def manager_view(request):

    p1 = booking.objects.using('odd').all()
    p2 = booking.objects.using('even').all()


    # Getting the count of all guest objects in the queryset
    p1_count = p1.count()
    p2_count = p2.count()
    count = p1_count + p2_count


    # getting count of Deluxe
    Deluxe_count_db1 = booking.objects.using('odd').filter(room_type='Deluxe').count()
    Deluxe_count_db2 = booking.objects.using('even').filter(room_type='Deluxe').count()
    Deluxe_count = Deluxe_count_db1 + Deluxe_count_db2

    #getting count of Standard
    Standard_count_db1 = booking.objects.using('odd').filter(room_type='Standard').count()
    Standard_count_db2 = booking.objects.using('even').filter(room_type='Standard').count()
    Standard_count = Standard_count_db1 + Standard_count_db2

   
    db1_count = booking.objects.using('odd').count()
    db2_count = booking.objects.using('even').count()


 


    params={'guest1': p1,
            'guest2': p2,
            'count':count,
            'Deluxe_count':Deluxe_count,
            'Standard_count': Standard_count,
            'db1_count': db1_count,
            'db2_count': db2_count,
           

            }

    return render(request, 'booking/manager_view.html', params)




def user_view(request):
    p1 = booking.objects.using('odd').all()
    p2 = booking.objects.using('even').all()

    return render(request, 'booking/user_view.html', {'guest1': p1, 'guest2': p2})


def user_details(request, pk):
    # Fetch all bookings for the particular guest ID (pk)
    bookings = booking.objects.using('even' if pk % 2 == 0 else 'odd').filter(guest_id=pk)

    params = {'bookings': bookings}

    return render(request, 'booking/user_details.html', params)

def analysis(request, pk):
    guest_id = pk

    # Retrieve guest bookings from either 'even' or 'odd' database based on guest_id
    guest_bookings = booking.objects.using('even' if pk % 2 == 0 else 'odd').filter(guest_id=guest_id)

    # Aggregate data to gain insights
    room_type_counts = guest_bookings.values('room_type').annotate(total=Count('room_type')).order_by('-total')
    total_spent = guest_bookings.aggregate(total_spent=Sum('total_cost'))['total_spent']
    average_spent_per_night = guest_bookings.aggregate(avg_price=Avg('price_per_night'))['avg_price']
    booking_frequencies = guest_bookings.dates('check_in_date', 'month', order='DESC').annotate(count=Count('id'))

    charts_data = [
        {'attribute': 'room_type', 'label': 'Room Type Preference', 'data': list(room_type_counts)},
        {'attribute': 'total_spent', 'label': 'Total Spent ($)', 'value': total_spent},
        {'attribute': 'avg_price_per_night', 'label': 'Average Price Per Night ($)', 'value': average_spent_per_night},
        {'attribute': 'booking_frequency', 'label': 'Booking Frequency Over Time', 'data': list(booking_frequencies)}
    ]

    context = {
        'guest_id': guest_id,
        'charts_data': charts_data
    }

    return render(request, 'booking/analysis.html', context)




def add(request):
    if request.method == "POST":
        booking_id = request.POST.get('booking_id')
        guest_id = request.POST.get('guest_id')
        full_name = request.POST.get('full_name')
        room_number = request.POST.get('room_number')
        room_type = request.POST.get('room_type')
        check_in_date = request.POST.get('check_in_date')
        check_out_date = request.POST.get('check_out_date')
        price_per_night = request.POST.get('price_per_night')
        total_cost = request.POST.get('total_cost')

        if not booking_id:
            # If booking ID is not provided, display error message
            messages.error(request, 'Booking ID is required')
            return render(request, 'booking/add.html')

        try:
            # Check if the booking_id already exists in either database
            booking_id = int(booking_id)
            #print (type(booking_id))
            booking_exists_even = booking.objects.using('even').filter(booking_id=booking_id).count() 
            booking_exists_odd = booking.objects.using('odd').filter(booking_id=booking_id).count()
            #print (booking_exists_even)
            #print (booking_exists_odd)
            if booking_exists_even > 0 or booking_exists_odd > 0:
                # Booking ID already exists, display error message
                messages.error(request, f'Booking ID {booking_id} already exists')
                return render(request, 'booking/add.html')

            else:
                database = 'odd' if int(guest_id) % 2 != 0 else 'even'

                new_booking = booking(
                    booking_id=booking_id,
                    guest_id=guest_id,
                    full_name=full_name,
                    room_number=room_number,
                    room_type=room_type,
                    check_in_date=check_in_date,
                    check_out_date=check_out_date,
                    price_per_night=price_per_night,
                    total_cost=total_cost
                )
                new_booking.save(using=database)

                print(f"""
                Booking ID: {booking_id}
                Guest ID: {guest_id}
                Full Name: {full_name}
                Room Number: {room_number}
                Room Type: {room_type}
                Check-in Date: {check_in_date}
                Check-out Date: {check_out_date}
                Price per Night: {price_per_night}
                Total Cost: {total_cost}
                Database: {database}
                """)

                # Set success message
                messages.success(request, 'Booking added successfully')
                return redirect('manager_view')
        except:
            print ('error')
        #except DatabaseError as e:
        #    # Handle database errors
        #    messages.error(request, f'Database error: {str(e)}')
        #    return render(request, 'booking/add.html')

    return render(request, 'booking/add.html')


def delete(request):
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        if booking_id:
            # Delete the booking from even database
            deleted_even = booking.objects.using('even').filter(booking_id=booking_id).delete()
            # Delete the booking from odd database
            deleted_odd = booking.objects.using('odd').filter(booking_id=booking_id).delete()
            if deleted_even[0] > 0 or deleted_odd[0] > 0:
                # At least one booking was deleted
                messages.success(request, 'Booking deleted successfully')
            else:
                # No booking was deleted
                messages.error(request, 'Booking not found')
                

    
    # Render the delete page
    return render(request, 'booking/delete.html')


#def update(request):
#    if request.method == "POST":
#        patient_id = request.POST.get('patient_id')
#        patient = Patient.objects.using('db2' if int(patient_id) % 2 == 0 else "db1").filter(patient_id=patient_id).get()
#        Patient.objects.using('db2' if int(patient_id) % 2 == 0 else "db1").filter(patient_id=patient_id).delete()
#
#        name = request.POST.get('name')
#        age = request.POST.get('age')
#        gender = request.POST.get('gender')
#        height = request.POST.get('height')
#        weight = request.POST.get('weight')
#        blood_type = request.POST.get('blood_type')
#        blood_pressure = request.POST.get('blood_pressure')
#        oxygen_level = request.POST.get('oxygen_level')
#        blood_sugar = request.POST.get('blood_sugar')
#        heart_rate = request.POST.get('heart_rate')
#        cholesterol = request.POST.get('cholesterol')
#        body_temperature = request.POST.get('body_temperature')
#        sleep_hours = request.POST.get('sleep_hours')
#        stress_level = request.POST.get('stress_level')
#
#        # Updating fields if provided
#        if name:
#            patient.name = name
#        if age:
#            patient.age = age
#        if gender:
#            patient.gender = gender
#        if height:
#            patient.height = height
#        if weight:
#            patient.weight = weight
#        if blood_type:
#            patient.blood_type = blood_type
#        if blood_pressure:
#            patient.blood_pressure = blood_pressure
#        if oxygen_level:
#            patient.oxygen_level = oxygen_level
#        if blood_sugar:
#            patient.blood_sugar = blood_sugar
#        if heart_rate:
#            patient.heart_rate = heart_rate
#        if cholesterol:
#            patient.cholesterol = cholesterol
#        if body_temperature:
#            patient.body_temperature = body_temperature
#        if sleep_hours:
#            patient.sleep_hours = sleep_hours
#        if stress_level:
#            patient.stress_level = stress_level
#
#
#        patient.save()
#
#        return redirect('manager_view')
#
#    params = {}
#    return render(request, 'insights/update.html', params)
