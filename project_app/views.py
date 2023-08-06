import json
from msilib import Table, add_data
from pyexpat.errors import messages
from urllib import response
import django
from django.shortcuts import render,  redirect
from django.http import HttpResponse, JsonResponse
from admin_app import models as model1
from project_app import models as model2
from datetime import datetime, time
from django.contrib import messages
from django.utils import timezone

# for pdf generation
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, Table
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib import colors

import pandas as pd
import openpyxl
import mysql.connector as connection

# Create your views here.


def security(request):
    if not request.session.has_key('loginData') or request.session['loginData'][2] != 'Security':
        return redirect('/')

    storage = messages.get_messages(request)
    storage.used = True
    print(list(messages.get_messages(request)))
    all_data = model1.Users.objects.filter(
        email=request.session['loginData'][0], password=request.session['loginData'][1]).values()

    markExit_data = model2.Security.objects.all().exclude(
        exit_time__isnull=False).values()

    return render(request, 'security.html', {'data': all_data[0], 'markExit_data': markExit_data})


def supervisor(request):
    if not request.session.has_key('loginData') or request.session['loginData'][2] != 'Supervisor':
        return redirect('/')

    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        id = request.GET.get('s')
        data = model2.Security.objects.filter(id=id).values()
        if data:
            return JsonResponse({'status': True, 'data': data[0]})
        else:
            return JsonResponse({'status': False})

    all_data = model1.Users.objects.filter(
        email=request.session['loginData'][0], password=request.session['loginData'][1]).values()
    # print(all_data[0]['department'])
    department = all_data[0]['department']
    markExit_data = model2.Supervisor.objects.filter(department=department).exclude(
        exit_time__isnull=False).values()

    mark = []
    req = []

    for worker in markExit_data:
        today = datetime.now()
        current_time = today.strftime('%H:%M:%S')
        current_time = datetime.strptime(current_time, '%H:%M:%S')

        entry_time = worker['entry_time']
        entry_time = entry_time.strftime('%H:%M:%S')
        entry_time = datetime.strptime(entry_time, '%H:%M:%S')

        diff = current_time - entry_time

        days = datetime.strptime(today.strftime("%Y-%m-%d"), "%Y-%m-%d") - \
            datetime.strptime(
                worker['entry_date'].strftime("%Y-%m-%d"), "%Y-%m-%d")

        if (diff.seconds // 3600) < 8 and days.days < 1:
            req.append(worker)
        else:
            model2.Supervisor.objects.filter(id=worker['id']).update(
                status='Completed')
            mark.append(worker)

    return render(request, 'supervisor.html', {'data': all_data[0], 'mark': mark, 'req': req})


def plantHead(request):
    if not request.session.has_key('loginData') or request.session['loginData'][2] != 'Plant head':
        return redirect('/')    
    
    id = request.COOKIES.get('id',None)
    filterType = request.COOKIES.get('type',None)
    value = request.COOKIES.get('value',None)
    
    ids = []
    departments = []
    all_workers = []
    pr_workers = []

    
    if filterType == None or filterType == '':
        if id == None or id == '':
            all_workers = model2.Security.objects.all().order_by('id').values()
            pr_workers = model2.Supervisor.objects.all().order_by('id').values()
        else:
            all_workers = model2.Security.objects.filter(w_id = id).values()
            pr_workers = model2.Supervisor.objects.filter(w_id = id).values()     
    
    else:
        if filterType == 'date' and value:
            value = datetime.strptime(value, "%Y-%m-%d").date()
            if(id):
                all_workers = model2.Security.objects.filter(w_id = id, entry_date__gte =  value).values()
                pr_workers = model2.Supervisor.objects.filter(w_id = id, entry_date = value).values()

            else:
                all_workers = model2.Security.objects.filter(entry_date__gte = value).values()
                pr_workers = model2.Supervisor.objects.filter(entry_date = value).values()
        
        elif filterType == 'month':
            value = datetime.strptime(value, "%Y-%m").date()
            
            if(id):
                all_workers = model2.Security.objects.filter(w_id = id, entry_date__month = value.month).values()
                pr_workers = model2.Supervisor.objects.filter(w_id = id, entry_date__month = value.month).values()

            else:
                all_workers = model2.Security.objects.filter(entry_date__month = value.month).values()
                pr_workers = model2.Supervisor.objects.filter(entry_date__month = value.month).values()
                
        elif filterType == 'week':
            week_num = value.split('W')[1]
            
            if(id):
                all_workers = model2.Security.objects.filter(w_id = id, entry_date__week = week_num).values()
                pr_workers = model2.Supervisor.objects.filter(w_id = id, entry_date__week = week_num).values()

            else:
                all_workers = model2.Security.objects.filter(entry_date__week = week_num).values()
                pr_workers = model2.Supervisor.objects.filter(entry_date__week = week_num).values()

    for worker in pr_workers:
        ids.append(worker['id'])
        if worker['department'] not in departments:
            departments.append(worker['department'])


    user_data = model1.Users.objects.filter(
        email=request.session['loginData'][0], password=request.session['loginData'][1]).values()
    requests = model2.Supervisor.objects.filter(status='Requested').values()
    context = {'length':len(all_workers),
                'all_workers': all_workers,
               'pr_workers': pr_workers,
               'requests': requests,
               'ids': ids,
               'departments': departments,
               'user': user_data[0]['name']}

    return render(request, 'planthead.html', context)


def addWorker(request):
    if request.method == 'POST':
        wid = request.POST.get('w_id')
        name = request.POST.get('name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        mobile = request.POST.get('mobile')
        aadhar = request.POST.get('aadhar')

        add = model2.Security(w_id = wid,name=name, age=age,
                              mobile=mobile, gender=gender, aadhar=aadhar)

        add.save()
        messages.success(request, 'Entry marked successfully!!!')
    return redirect('/')


def updateWorker(request):
    try:
        if request.method == 'POST':
            id = request.POST.get('id')
            w_id = request.POST.get('w_id')
            name = request.POST.get('name')
            age = request.POST.get('age')
            gender = request.POST.get('gender', 'Male')
            mobile = request.POST.get('mobile')
            aadhar = request.POST.get('aadhar')

            email = request.session['loginData'][0]
            data = model1.Users.objects.filter(email=email).values()

            add = model2.Supervisor(w_id=w_id,id=id, name=name, age=age,
                                    mobile=mobile, gender=gender, aadhar=aadhar, department=data[0]['department'])
            messages.success(request, 'Entry marked successfully!!!')
            add.save()

    except:
        messages.error(request, 'Entry already marked!!!')
        return redirect('/')
    return redirect('/')


def markExit(request):
    ids = request.GET.get('ids')
    print(ids)
    ids = ids.split(',')
    print(type(ids), ids)

    current_url = request.path
    print(current_url)

    if current_url == '/project/security/markExit/':
        if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
            for id in ids:
                print(id)
                model2.Security.objects.filter(id=id).update(
                    exit_time=datetime.now().strftime('%H:%M:%S'))
        print(current_url)
        storage = messages.get_messages(request)
        storage.used = True
        messages.success(request, 'Out Time Marked Successfully!!!')
        return JsonResponse({'status': True})

    else:
        if current_url == '/project/plantHead/markExit/':
            for id in ids:
                model2.Supervisor.objects.filter(id=id).update(
                status='Completed')
        elif request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
            for id in ids:
                model2.Supervisor.objects.filter(id=id).update(
                    exit_time=datetime.now().strftime('%H:%M:%S'))
            storage = messages.get_messages(request)
            storage.used = True
        messages.success(request, 'Out Time Marked Successfully!!!')

        return JsonResponse({'status': True})


def requestExit(request):
    print('You are in req function')
    id = request.GET.get('ids', '')

    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            model2.Supervisor.objects.filter(id=id).update(
                status='Requested')
            storage = messages.get_messages(request)
            storage.used = True
            messages.success(request, 'Requested Successfully !!!')
        except:
            print('Error Occured')
            return JsonResponse({'status': False})

    return JsonResponse({'status': True})


def cancelRequest(request):
    print('You are in cancel func')
    id = request.GET.get('ids', '')

    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            status = model2.Supervisor.objects.filter(id=id).values()[
                0]['status']
            if status == 'Requested':
                model2.Supervisor.objects.filter(
                    id=id).update(status='Request')
        except Exception as e:
            return JsonResponse({'status': False, 'exception': e})

    return JsonResponse({'status': True})

def requests(request):
    requests_var = model2.Supervisor.objects.filter(status='Requested').values()
    print(requests_var)
    print(len(requests_var))
    return JsonResponse({'requests': list(requests_var),'reqLength':len(requests_var)})

def latestEntries(request):
    print("Inside latest entries")
    ids = model2.Supervisor.objects.values_list('id')
    print(ids)
    latestEntries = model2.Security.objects.filter(entry_date = datetime.today()).exclude(id__in=ids).values()
    print(latestEntries)
    return JsonResponse({'latestEntries': list(latestEntries)})

def pdf(request):
    if(request.GET.get('name') == 'security'):
        try:
            mydb = connection.connect(host="localhost", database = 'wms',user="prajval", passwd="P@ju3152",use_pure=True)
            query = "Select * from project_app_security;"
            result_dataFrame = pd.read_sql(query,mydb)
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            filename=f"Security_all_{timezone.now()}.xlsx"
            response['Content-Disposition'] = 'attachment; filename='+filename                                        
            result_dataFrame.to_excel(response)
            mydb.close() #close the connection
            return response
        except Exception as e:
            mydb.close()
            print(str(e)) 
        

    elif(request.GET.get('name') == 'supervisor'):
        try:
            mydb = connection.connect(host="localhost", database = 'wms',user="prajval", passwd="P@ju3152",use_pure=True)
            query = "Select * from project_app_supervisor;"
            result_dataFrame = pd.read_sql(query,mydb)
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            filename=f"Supervisor_all_{timezone.now()}.xlsx"
            response['Content-Disposition'] = 'attachment; filename='+filename                                        
            result_dataFrame.to_excel(response)
            mydb.close() #close the connection
            return response
        except Exception as e:
            mydb.close()
            print(str(e)) 

    else:
        department = request.GET.get('name')

        try:
            mydb = connection.connect(host="localhost", database = 'wms',user="prajval", passwd="P@ju3152",use_pure=True)
            query = "Select * from project_app_supervisor where department='"+department+"';"
            result_dataFrame = pd.read_sql(query,mydb)
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            filename=f"Security_{department}_{timezone.now()}.xlsx"
            response['Content-Disposition'] = 'attachment; filename='+filename                                        
            result_dataFrame.to_excel(response)
            mydb.close() #close the connection
            return response
        except Exception as e:
            mydb.close()
            print(str(e)) 

# def pdf(request):
#     buf = io.BytesIO()
#     c = canvas.Canvas(buf, pagesize=letter, bottomup=0)

#     textob = c.beginText(50, 100)
#     textob.setTextOrigin(inch, inch)
#     textob.setFont("Helvetica", 14)

#     tableData = []

#     if(request.GET.get('name') == 'security'):
#         securityData = model2.Security.objects.all().values()
#         securityData = list(securityData)

#         # print(securityData)
#         # print(list(securityData))
#         df = pd.DataFrame(list(securityData),
#                     columns=['ID', 'Name', 'Age',
#                         'Gender', 'Mobile', 'Aadhar', 'Entry Date', 'Entry Time', 'Exit Time'])

#         # print(df)
#         tableData = [['ID', 'Name', 'Age',
#                       'Gender', 'Mobile', 'Aadhar', 'Entry Date', 'Entry Time', 'Exit Time']]

#         for data in securityData:
#             tableData.append(list(data.values()))

#         table = Table(tableData[::-1], style=[
#             ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
#             ('Helvetica', (0, 0), (0, 5), 'Courier-Bold'),
#             ('BOX', (0, 0), (-1, -1),
#              2, colors.black),
#             ('GRID', (0, 0), (-1, -1),
#              1, colors.black),
#             ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
#             ('TOPPADDING', (0, 0), (-1, -1), 3),
#         ])

#         table._argW[3] = 1*inch
#         for i in range(len(tableData)):
#             table._argH[i] = .5*inch

#         textob.textLine("Security Records")
#         c.drawText(textob)
#         table.wrapOn(c, 50, 50)
#         table.drawOn(c, 50, 150)

#         c.setTitle('Security Records')
#         c.showPage()
#         c.save()
#         buf.seek(0)
#         return FileResponse(buf, as_attachment=True, filename=f"Security_all_{timezone.now()}.pdf")

#     elif(request.GET.get('name') == 'supervisor'):
#         supervisorData = model2.Supervisor.objects.all().values()
#         supervisorData = list(supervisorData)

#         tableData = [['ID', 'Name', 'Age',
#                       'Gender', 'Mobile', 'Aadhar', 'Department', 'Entry Date', 'Entry Time', 'Exit Time']]

#         for data in supervisorData:
#             tableData.append(list(data.values()))

#         table = Table(tableData[::-1], style=[
#             ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
#             ('Helvetica', (0, 0), (0, 5), 'Courier-Bold'),
#             ('BOX', (0, 0), (-1, -1),
#              2, colors.black),
#             ('GRID', (0, 0), (-1, -1),
#              1, colors.black),
#             ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
#             ('TOPPADDING', (0, 0), (-1, -1), 3),
#         ])

#         table._argW[3] = .6*inch
#         table._argW[4] = .9*inch
#         table._argW[5] = 1.05*inch
#         table._argW[7] = .85*inch
#         table._argW[8] = .75*inch
#         table._argW[9] = .75*inch
#         for i in range(len(tableData)):
#             table._argH[i] = .5*inch

#         textob.textLine("Supervisor Records")
#         c.drawText(textob)
#         table.wrapOn(c, 50, 50)
#         table.drawOn(c, 50, 150)
#         c.setTitle('Supervisor Records')
#         c.showPage()
#         c.save()
#         buf.seek(0)
#         return FileResponse(buf, as_attachment=True, filename=f"Supervisor_all_{timezone.now()}.pdf")

#     else:
#         department = request.GET.get('name')
#         departmentData = model2.Supervisor.objects.filter(
#             department=department).values()
#         departmentData = list(departmentData)

#         tableData = [['ID', 'Name', 'Age',
#                       'Gender', 'Mobile', 'Aadhar', 'Entry Date', 'Entry Time', 'Exit Time']]

#         for data in departmentData:
#             data.pop('department')
#             tableData.append(list(data.values()))

#         table = Table(tableData[::-1], style=[
#             ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
#             ('Helvetica', (0, 0), (0, 5), 'Courier-Bold'),
#             ('BOX', (0, 0), (-1, -1),
#              2, colors.black),
#             ('GRID', (0, 0), (-1, -1),
#              1, colors.black),
#             ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
#             ('TOPPADDING', (0, 0), (-1, -1), 3),
#         ])

#         table._argW[3] = 1*inch
#         for i in range(len(tableData)):
#             table._argH[i] = .5*inch

#         textob.textLine(f"{department.capitalize()} Records")
#         c.drawText(textob)
#         table.wrapOn(c, 50, 50)
#         table.drawOn(c, 50, 150)
#         c.setTitle(f'{department.capitalize()} Records')
#         c.showPage()
#         c.save()
#         buf.seek(0)
#         return FileResponse(buf, as_attachment=True, filename=f"Department_{department.capitalize()}_{timezone.now()}.pdf")

