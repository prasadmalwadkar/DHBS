# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, request
from django.shortcuts import get_object_or_404
from django.db.models import F
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import booking



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


    # sleep speedometer
   # sleep_hrs_list=[]
   # sleep_db1 = Patient.objects.using('db1').all()
   # sleep_db2 = Patient.objects.using('db2').all()
#
   # for p in sleep_db1:
   #     sleep_hrs_list.append(p.sleep_hours)
   # for p in sleep_db2:
   #     sleep_hrs_list.append(p.sleep_hours)
#
   # sleep_hrs_list=sorted(sleep_hrs_list)
   # average_sleep = sum(sleep_hrs_list) / len(sleep_hrs_list) if sleep_hrs_list else 0
#
   # # stress speedometer
   # stress_list=[]
   # for p in sleep_db1:
   #     stress_list.append(p.stress_level)
   # for p in sleep_db2:
   #     stress_list.append(p.stress_level)
#
   # stress_list = sorted(stress_list)
   # average_stress = sum(stress_list) / len(stress_list)
#
   # # weight gauge
   # weight_list=[]
   # for p in sleep_db1:
   #     weight_list.append(p.cholesterol)
   # for p in sleep_db2:
   #     weight_list.append(p.cholesterol)
   # weight_list=sorted(weight_list)
   # average_weight =sum(weight_list) / len(weight_list)
#
   # # hight gauge
   # height_list=[]
   # for p in sleep_db1:
   #     height_list.append(p.oxygen_level)
   # for p in sleep_db2:
   #     height_list.append(p.oxygen_level)
   # height_list=sorted(height_list)
   # average_height =sum(height_list) / len(height_list)


    params={'guest1': p1,
            'guest2': p2,
            'count':count,
            'Deluxe_count':Deluxe_count,
            'Standard_count': Standard_count,
           # 'underweight_count':underweight_count,
           # 'idealweight_count':idealweight_count,
           # 'overweight_count':overweight_count,
           # 'obese_class1_count':obese_class1_count,
           # 'obese_class2_count':obese_class2_count,
           # 'obese_class3_count':obese_class3_count,
            'db1_count': db1_count,
            'db2_count': db2_count,
           # 'sleep_hours':sleep_hrs_list,
           # 'average_sleep': average_sleep,
           # 'stress_list':stress_list,
           # 'average_stress':average_stress,
           # 'weight_list':weight_list,
           # 'average_weight':average_weight,
           # 'height_list':height_list,
           # 'average_height':average_height

            }

    return render(request, 'booking/manager_view.html', params)


'''def manager_graphs(request):

    x_list = []
    y_list=[]
    x_axis ='null'
    y_axis='null'

    if request.method == 'POST':
        x_axis = request.POST.get('xaxis')
        y_axis = request.POST.get('yaxis')
        graph_type = request.POST.get('graph')



        print('Received x-axis value:', x_axis)
        print('Received y-axis value:', y_axis)

        # Querying the Patient objects using a specified database
        patients1 = Patient.objects.using('db1').all()

        # Assuming you want to print the value of attributes in patients that are named similarly to x_axis and y_axis dynamically
        for patient in patients1:
            # Safely getting attribute values based on string names with default fallback
            patient_x_value = getattr(patient, x_axis, "Attribute not found")
            x_list.append(patient_x_value)
            patient_y_value = getattr(patient, y_axis, "Attribute not found")
            y_list.append(patient_y_value)

        patients2 = Patient.objects.using('db2').all()

        for patient in patients2:
            # Safely getting attribute values based on string names with default fallback
            patient_x_value = getattr(patient, x_axis, "Attribute not found")
            x_list.append(patient_x_value)
            patient_y_value = getattr(patient, y_axis, "Attribute not found")
            y_list.append(patient_y_value)

    params={'xlabel':x_axis,
            'ylabel':y_axis,
            'x_list':x_list,
            'y_list':y_list,
            'graph': graph_type
            }
    return render(request,'insights/manager_graphs.html',params)  '''

def user_view(request):
    p1 = booking.objects.using('odd').all()
    p2 = booking.objects.using('even').all()

    return render(request, 'booking/user_view.html', {'guest1': p1, 'guest2': p2})


def user_details(request, pk):
    # Fetch all bookings for the particular guest ID (pk)
    bookings = booking.objects.using('even' if pk % 2 == 0 else 'odd').filter(guest_id=pk)

    params = {'bookings': bookings}

    return render(request, 'booking/user_details.html', params)

def booking_analysis(request, pk):
    guest_id = pk

    # Retrieve guest bookings from either 'even' or 'odd' database based on guest_id
    guest_bookings = Booking.objects.using('even' if pk % 2 == 0 else 'odd').filter(guest_id=guest_id)

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


#def analysis(request,pk):
#    id = pk
#
#    myguest = booking.objects.using('even' if pk % 2 == 0 else 'odd').filter(guest_id=id).get()
#
#    odd_data = booking.objects.using('db1').filter(gender = mypatient.gender).all()
#
#    db2_data = Patient.objects.using('db2').filter(gender=mypatient.gender).all()
#
#    all_heights = list(db1_data.values_list('height', flat=True)) + list(db2_data.values_list('height', flat=True))
#    all_weights = list(db1_data.values_list('weight', flat=True)) + list(db2_data.values_list('weight', flat=True))
#    all_blood_pressures = list(db1_data.values_list('blood_pressure', flat=True)) + list(db2_data.values_list('blood_pressure', flat=True))
#    all_oxygen_levels = list(db1_data.values_list('oxygen_level', flat=True)) + list(db2_data.values_list('oxygen_level', flat=True))
#    all_heart_rates = list(db1_data.values_list('heart_rate', flat=True)) + list(db2_data.values_list('heart_rate', flat=True))
#
#    def aggregate_data(attribute):
#        return list(db1_data.values_list(attribute, flat=True)) + list(db2_data.values_list(attribute, flat=True))
#
#    charts_data = [
#        {'attribute': 'height', 'label': 'Height in inches', 'values': aggregate_data('height'), 'user_value': mypatient.height},
#        {'attribute': 'weight', 'label': 'Weight in pounds', 'values': aggregate_data('weight'), 'user_value': mypatient.weight},
#        {'attribute': 'blood_pressure', 'label': 'Blood Pressure in mmHg', 'values': aggregate_data('blood_pressure'), 'user_value': mypatient.blood_pressure},
#        {'attribute': 'oxygen_level', 'label': 'Oxygen Level in %', 'values': aggregate_data('oxygen_level'), 'user_value': mypatient.oxygen_level},
#        {'attribute': 'heart_rate', 'label': 'Heart Rate in bpm', 'values': aggregate_data('heart_rate'), 'user_value': mypatient.heart_rate},
#        {'attribute': 'blood_sugar', 'label': 'Blood Sugar in mg/dL', 'values': aggregate_data('blood_sugar'), 'user_value': mypatient.blood_sugar},        {'attribute': 'sleep_hours', 'label': 'Sleep Hours per Night', 'values': aggregate_data('sleep_hours'), 'user_value': mypatient.sleep_hours},
#        {'attribute': 'stress_level', 'label': 'Stress Level', 'values': aggregate_data('stress_level'), 'user_value': mypatient.stress_level}
#    ]
#
#    context = {
#        'patient': mypatient,
#        'charts_data': charts_data
#    }
#
#    return render(request,'insights/analysis.html', context)


#def bmi_calculation(height, weight):
#    height_m = height / 100.0
#    weight_kg = weight * 0.453592
#
#    bmi = weight_kg / (height_m ** 2)
#
#    return float(bmi)


def add(request):
    if request.method == "POST":
        guest_id = request.POST.get('guest_id')
        full_name = request.POST.get('full_name')
        room_number = request.POST.get('room_number')
        room_type = request.POST.get('room_type')
        check_in_date = request.POST.get('check_in_date')
        check_out_date = request.POST.get('check_out_date')
        price_per_night = request.POST.get('price_per_night')
        total_cost = request.POST.get('total_cost')

        database = 'odd' if int(guest_id) % 2 != 0 else 'even'

        new_booking = booking(
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

        return redirect('manager_view')

    return render(request, 'booking/add.html')

def delete(request):
    if request.method == "POST":
        guest_id = request.POST.get('guest_id')

        if int(guest_id) % 2 == 0:
            bookings = booking.objects.using('even').filter(guest_id=guest_id)
        else:
            bookings = booking.objects.using('odd').filter(guest_id=guest_id)

        # Delete all bookings for the specified guest_id
        for booking in bookings:
            booking.delete()

        return redirect('manager_view')
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
