from django.shortcuts import render
from django.http import HttpResponse
from dashboard.models import Attendance, IdentityCard
from datetime import date
import base64

# Create your views here.
def api_interface(request):
    return render(request, 'api/interface.html')

def mark_attendance(request, gr_no):   
    gr_no = base64.b64decode(gr_no.encode("ascii")).decode("ascii")
    if len(IdentityCard.objects.filter(gr_no=gr_no)) == 1:
        student = IdentityCard.objects.get(gr_no=gr_no)
        first_name = student.name.split()[0]
        if len(Attendance.objects.filter(student=student, date=str(date.today()))) == 0:
            attendance_obj = Attendance.objects.create(student=student, date=str(date.today()))
            attendance_obj.save()
            return HttpResponse(f'A very good morning {first_name}!')
        else:    
            return HttpResponse(f'Your attendance is already marked, {first_name}')
    else:
        return HttpResponse('G.R. number not found.')


def download_spreadsheet(request):
    if request.method == 'POST':
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
            return render(request, "dashboard/spreadsheet.html") 
    else:
        return render(request, 'dashboard/login.html')