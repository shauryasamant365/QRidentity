from datetime import datetime
from django.shortcuts import render, redirect
from .models import Birthday
from dashboard.models import IdentityCard

# Create your views here.
def index(request):
    # Get birthdays
    birthday_guys = IdentityCard.objects.get_birthdays()        
    if len(birthday_guys) == 0:
        birthdays = 'null'
    else:
        birthdays = 'there'
    birthday_guys_list = []
    first_names = []
    for item in birthday_guys:
        birthday_guy = [item.picture, item.name, item.standard, item.division, item.dob, 'STUDENT']
        first_names.append(item.name.split()[0])
        birthday_guys_list.append(birthday_guy)
    print(birthday_guys)
    print(birthdays)
    return render(request, 'birthday/index.html', {'first_names': first_names,'birthday_guys': birthday_guys_list, 'birthdays': birthdays})
    

def add(request):
    if request.method == 'POST':
        name = request.POST['name']
        dob = str(request.POST['dob'])[2:]
        dob = datetime.strptime(dob, '%y-%m-%d')
        if len(Birthday.objects.filter(name=name, dob=dob)) == 0:
            Birthday.objects.create(name=name, dob=dob)
            # Get birthdays
            birthday_guys = IdentityCard.objects.get_birthdays()        
            if len(birthday_guys) == 0:
                birthdays = 'null'
            else:
                birthdays = 'there'
            birthday_guys_list = []
            first_names = []
            for item in birthday_guys:
                birthday_guy = [item.picture, item.name, item.standard, item.division, item.dob, 'STUDENT']
                first_names.append(item.name.split()[0])
                birthday_guys_list.append(birthday_guy)
            print(birthday_guys)
            print(birthdays)
            return render(request, 'birthday/index.html', {'first_names': first_names,'birthday_guys': birthday_guys_list, 'birthdays': birthdays, 'msg': True, 'content': 'Your birhday has been added successfully!'})
        else:
            # Get birthdays
            birthday_guys = IdentityCard.objects.get_birthdays()        
            if len(birthday_guys) == 0:
                birthdays = 'null'
            else:
                birthdays = 'there'
            birthday_guys_list = []
            first_names = []
            for item in birthday_guys:
                birthday_guy = [item.picture, item.name, item.standard, item.division, item.dob, 'STUDENT']
                first_names.append(item.name.split()[0])
                birthday_guys_list.append(birthday_guy)
            print(birthday_guys)
            print(birthdays)
            return render(request, 'birthday/index.html', {'first_names': first_names,'birthday_guys': birthday_guys_list, 'birthdays': birthdays, 'msg': True, 'content': 'Your birhday already exists, check the name spelling and birthdate and try again!'})
    else:
        return redirect('birthday_index')
