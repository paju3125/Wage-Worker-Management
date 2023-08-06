import email
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import redirect, render

from project_app.views import supervisor
from . import models
from django.contrib import messages
# Create your views here.

def index(request):
    if not request.session.has_key('loginData') or request.session['loginData'][2] != 'Admin':
        return redirect('/')

    all_data = models.Users.objects.all()
    dept_data = models.Departments.objects.all()
    number_of_users = [0,0,0,0]
    
    p_id = sv_id = sc_id = 0
    for user in all_data:
        if(user.designation == 'Admin'):
            number_of_users[0] = number_of_users[0]+1
        
        if(user.designation == 'Plant head'):
            number_of_users[1] = number_of_users[1]+1
            if user.id > p_id:
                p_id = user.id

        if(user.designation == 'Supervisor'):
            number_of_users[2] = number_of_users[2]+1
            if user.id > sv_id:
                sv_id = user.id

        if(user.designation == 'Security'):
            number_of_users[3] = number_of_users[3]+1
            if user.id > sc_id:
                sc_id = user.id

        if(user.email == request.session['loginData'][0]):
            loggedUser = user.name

    no_users = {
        'users' :sum(number_of_users),
        'admins':number_of_users[0],
        'planthead':number_of_users[1],
        'supervisor':number_of_users[2],
        'security':number_of_users[3],
        'depts' : len(dept_data)
    }
    
    return render(request, 'admin_app/admin.html', {'users': all_data,'no_users':no_users, 'p_id': p_id+1, 'sv_id': sv_id+1, 'sc_id': sc_id+1, 'loggedUser': loggedUser, 'departments':dept_data})


def addplant(request):
    if request.method == 'POST':
        id = (int(request.POST.get("id")))
        name = request.POST.get("name")
        mobile = int(request.POST.get("mobile"))
        email = request.POST.get("email")
        password = request.POST.get("password")
        gender = request.POST.get("gender")
        designation = request.POST.get("designation")
        add = models.Users(id=id, name=name, mobile=mobile, email=email, password=password,
                           gender=gender, designation=designation)

        add.save()
    return redirect('/admin/')


def addsupervisor(request):
    if request.method == 'POST':
        id = (int(request.POST.get("id")))
        name = request.POST.get("name")
        mobile = int(request.POST.get("mobile"))
        email = request.POST.get("email")
        password = request.POST.get("password")
        gender = request.POST.get("gender")
        designation = request.POST.get("designation")
        department = request.POST.get("department")
        add = models.Users(id=id, name=name, mobile=mobile, email=email, password=password,
                           gender=gender, designation=designation, department=department)
        add.save()

        # Cursor = connection.cursor()
        # Cursor.execute(f"create table supervisor_{id} (name varchar(50))")
    return redirect('/admin/')

def addsecurity(request):
    if request.method == 'POST':
        id = (int(request.POST.get("id")))
        name = request.POST.get("name")
        mobile = int(request.POST.get("mobile"))
        email = request.POST.get("email")
        password = request.POST.get("password")
        gender = request.POST.get("gender")
        designation = request.POST.get("designation")
        add = models.Users(id=id, name=name, mobile=mobile, email=email, password=password,
                           gender=gender, designation=designation)

        add.save()
    return redirect('/admin/')


def updateplant(request):
    if request.method == 'POST':
        id = (int(request.POST.get("id")))
        name = request.POST.get("name")
        mobile = int(request.POST.get("mobile"))
        email = request.POST.get("email")
        password = request.POST.get("password")
        gender = request.POST.get("gender")

        Cursor = connection.cursor()
        if password == "":
            Cursor.execute(
                f"update admin_app_users set name='{name}',gender='{gender}',mobile={mobile}, email='{email}' where id={id} and designation='Plant head'")

        else:
            Cursor.execute(
                f"update admin_app_users set name='{name}',gender='{gender}',mobile={mobile}, email='{email}', password='{password}' where id={id} and designation='Plant head'")

    return redirect('/admin/')


def updatesupervisor(request):
    if request.method == 'POST':
        id = (int(request.POST.get("id")))
        name = request.POST.get("name")
        mobile = int(request.POST.get("mobile"))
        email = request.POST.get("email")
        password = request.POST.get("password")
        gender = request.POST.get("gender")
        department = request.POST.get("department")

        Cursor = connection.cursor()
        if password == "":
            Cursor.execute(
                f"update admin_app_users set name='{name}',gender='{gender}',mobile={mobile}, email='{email}', department='{department}' where id={id} and designation='Supervisor'")

        else:
            Cursor.execute(
                f"update admin_app_users set name='{name}',gender='{gender}',mobile={mobile}, email='{email}', password='{password}', department='{department}' where id={id} and designation='Supervisor'")

    return redirect('/admin/')


def updatesecurity(request):
    if request.method == 'POST':
        id = (int(request.POST.get("id")))
        name = request.POST.get("name")
        mobile = int(request.POST.get("mobile"))
        email = request.POST.get("email")
        password = request.POST.get("password")
        gender = request.POST.get("gender")

        Cursor = connection.cursor()
        if password == "":
            Cursor.execute(
                f"update admin_app_users set name='{name}',gender='{gender}',mobile={mobile}, email='{email}' where id={id} and designation='Security'")

        else:
            Cursor.execute(
                f"update admin_app_users set name='{name}',gender='{gender}',mobile={mobile}, email='{email}', password='{password}' where id={id} and designation='Security'")

    return redirect('/admin/')


def deleteuser(request):
    if request.method == 'POST':
        id = int(request.POST.get("id"))
        designation = request.POST.get("designation").capitalize()

        Cursor = connection.cursor()
        Cursor.execute(
            f"delete from admin_app_users where id={id} and designation='{designation}'")

        # if(designation == "Security" or designation == "Supervisor"):
        #     Cursor.execute(
        #         f"drop table {designation.lower()}_{id}")

    return redirect('/admin/')

def adddept(request):
    if request.method == 'POST':
        deptName = request.POST.get("deptName")
        add = models.Departments(dept_name = deptName)
        print(add)
        print(add.save())
        messages.success(request, 'New department added successfully!!!\n Department : '+deptName)
    return redirect('/admin/')

def deletedept(request):
    if request.method == 'POST':
        id = request.POST.get("deptName")
        models.Departments.objects.filter(id = id).delete()
        messages.success(request, 'Department deleted successfully!!!')
    return redirect('/admin/')