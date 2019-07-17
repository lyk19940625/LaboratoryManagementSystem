from django.shortcuts import render
from django.shortcuts import render,render_to_response,redirect
from django.shortcuts import HttpResponse,HttpResponseRedirect
from django import forms
from LMS.models import User
from LMS.models import  Task
from LMS.models import StudentTask
from django.http import JsonResponse
from LaboratoryManagementSystem import settings
from django.http import StreamingHttpResponse
import os
from django.contrib.sessions.models import Session
from random import choice
# Create your views here.

class RegisterForm(forms.Form):
    uid = forms.CharField(max_length=15)
    uname = forms.CharField(max_length=8)
    password = forms.CharField(max_length=30)
    type = forms.CharField(max_length=8)
    room = forms.CharField(max_length=8)
    sex = forms.CharField(max_length=2)
    class_field = forms.CharField(max_length=8)
    birthday = forms.CharField(max_length=8)
    photo = forms.CharField(max_length=50)
    tel = forms.CharField(max_length=11)
    email = forms.EmailField()


class LoginForm(forms.Form):
    uid = forms.CharField(max_length=15)
    password = forms.CharField(max_length=30)


def login(req):
    return render(req, 'login.html')
    # print req.method


def loginVerify(request):
    # return JsonResponse({'res':request.POST.get('username')})
    if request.method == 'POST':
        uid = request.POST.get('uid')
        password = request.POST.get('password')
        print(uid,password)
        try:
            user = User.objects.get(uid=uid)
            if (uid == "111"):
                return JsonResponse({'res': 2})
            if (user.password == password):
                request.session['uname'] = user.uname
                request.session['uid'] = user.uid
                type = user.type
                if(type == 'student'):
                    return JsonResponse({'res': 1})
                if (type == 'manager'):
                    return JsonResponse({'res': 2})
            else:
                return JsonResponse({'res': 0})
        except:
            return JsonResponse({'res': -1})
    return JsonResponse({'res': 100})


def logout(request):
    try:
        del request.session['uid']
    except KeyError:
        pass
    return redirect('/')





def inregister(request):
    return render(request,'register.html')


def register(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        password = request.POST.get('password')
        uname = request.POST.get('uname')
        type = request.POST.get('type')
        room = request.POST.get('room')
        sex = request.POST.get('sex')
        class_field = request.POST.get('class_field')
        birthday = request.POST.get('birthday')
        tel = request.POST.get('tel')
        email = request.POST.get('email')
        filterResult = User.objects.filter(uid=uid)
        if (len(filterResult) > 0):
            return JsonResponse({'res': 1})
        else:
            user = User.objects.create(uid=uid,uname=uname,password=password,email=email,type=type,room=room,sex=sex,class_field=class_field,birthday=birthday,tel=tel)
            user.save()
            return JsonResponse({'res': 0})
    return JsonResponse({'res': 100})

def index(request):
    uname = request.session.get('uname')
    return render_to_response('index.html', {'uname':uname})

def allTask(req):
    uname = req.session.get('uname')
    print(uname)
    tasks = Task.objects.filter(finish='发布中')
    return render_to_response('allTask.html', locals())
    # print req.method

def acceptTask(request):
    if request.method == 'POST':
        uname = request.session.get('uname')
        tid = request.POST.get('tid')
        task = Task.objects.get(tid=tid)
        sList = task.students.split(',')
        if uname in sList:
            return  JsonResponse({'res': 1})
        task.students = task.students + uname + ','
        task.save()
        return JsonResponse({'res': 0})
    return JsonResponse({'res': 100})

def abandonTask(request):
    if request.method == 'POST':
        uname = request.session.get('uname')
        tid = request.POST.get('tid')
        print(uname)
        print(tid)
        task = Task.objects.get(tid=tid)
        sList = task.students.split(',')
        if uname in sList:
            sList.remove('')
            sList.remove(uname)
            print(sList)
            students = ''
            for student in sList:
                students = student + ','
            task.students = students
            task.save()
            return JsonResponse({'res': 0})
        else:
            return JsonResponse({'res': 1})
    return JsonResponse({'res': 100})
'''
def adminWork(req):
    uname = req.session.get('uname')
    tasks = Task.objects.filter(finish='1')
    myTasks = []
    for task in tasks:
        students = task.students.split(',').remove('')
        if uname in students:
            myTasks.append(task)
    return render_to_response('adminWork.html', locals())
'''
def myWork(req):
    uid = req.session.get('uid')
    uname = req.session.get('uname')
    tasks = StudentTask.objects.filter(uid=uid)
    return render_to_response('myWork.html', locals())

def upload_ajax(request):
    uid = request.session.get('uid')
    if request.method == 'POST':
        file_obj = request.FILES.get('file')
        tid = request.POST.get('tid')
        print(tid)
        file_path = os.path.join(settings.BASE_DIR, 'upload', tid)
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        f = open(os.path.join(file_path, file_obj.name), 'wb')
        print(file_path)
        print(file_obj,type(file_obj))
        for chunk in file_obj.chunks():
            f.write(chunk)
        f.close()
        sid = int(str(uid) + tid)
        studentTask = StudentTask.objects.get(sid=sid)
        if studentTask.path == None:
            studentTask.path = file_obj.name + ','
        else:
            studentTask.path = studentTask.path + file_obj.name + ','
        studentTask.save()
        task = Task.objects.get(tid=tid)
        if task.path == None:
            task.path = file_obj.name + ','
        else:
            task.path = task.path + file_obj.name + ','
        task.save()
        return HttpResponse('OK')

def getWorkId(req):
    if req.method == 'POST':
        global workId
        workId = req.POST.get('sid')
        print(workId)
        return JsonResponse({'res': 1})
    return JsonResponse({'res': 100})

def eachWork(req):
    uid = req.session.get('uid')
    uname = req.session.get('uname')
    print(workId)
    studentTask = StudentTask.objects.get(sid=workId)
    task = Task.objects.get(tid=studentTask.tid)
    files = task.path.split(',')
    task2 = StudentTask.objects.filter(tid=studentTask.tid)
    return render_to_response('eachWork.html', locals())

def editMyWork(req):
    if req.method == 'POST':
        tname = req.POST.get('tname')
        work = req.POST.get('work')
        percent = int(req.POST.get('percent'))
        content = req.POST.get('content')
        progress = req.POST.get('progress')
        studentTask = StudentTask.objects.get(sid=workId)
        studentTask.sname = tname+'#'+work
        studentTask.content = content
        value = int(Task.objects.get(tid=studentTask.tid).value)*percent
        studentTask.value = int(value/100)
        studentTask.progress = progress
        studentTask.save()

        allSW = StudentTask.objects.filter(tid=studentTask.tid)
        p = 0
        for s in allSW:
            p = int(s.progress/len(allSW)) + p
        newTask = Task.objects.get(tid=studentTask.tid)
        newTask.progress = p
        newTask.save()
        return JsonResponse({'res': 1})

    return JsonResponse({'res': 100})

def getFileInfo(request):
    if request.method == 'POST':
        download_name = request.POST.get('fileName')
        tid = request.POST.get('taskID')
        global fileInfo
        fileInfo = tid+r'/'+download_name
        #download_file(download_name, tid)
    return JsonResponse({'res': 1})

def download_file(request):
    the_file_name = str(fileInfo.split('/')[1]).split("/")[-1]  # 显示在弹出对话框中的默认的下载文件名
    print(the_file_name)
    #filename = r'G:/PythonWorkSpace/Django/LaboratoryManagementSystem/upload/1/django.txt'
    filename = os.path.join(settings.BASE_DIR, 'upload').replace('\\','/')+'/'+ fileInfo # 要下载的文件路径
    print(filename)
    response = StreamingHttpResponse(readFile(filename))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
    return  response
def readFile(filename, chunk_size=512):
    """
    缓冲流下载文件方法
    :param filename:
    :param chunk_size:
    :return:
    """
    with open(filename, 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break


def attendance(req):
    if req.COOKIES.get('cookie_uname', ''):
        uname = req.COOKIES.get('cookie_uname', '')
    else:
        return HttpResponseRedirect("login")
    Method = req.method
    curtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    date = now().date() + timedelta(days=0)
    global start_time
    global end_time
    global start
    if Method == 'POST':
        if 'start' in req.POST:
            start_time = time.strftime("%H:%M:%S", time.localtime())

            start = datetime.datetime.now()
            response = HttpResponseRedirect('index')
            response.set_cookie('cookie_start_time', start_time)
            return response

        if 'end' in req.POST:
            end_time = time.strftime("%H:%M:%S", time.localtime())

            end = datetime.datetime.now()
            time_length = (end - start).seconds

            time_add = DailyTime.objects.create(id=curtime, date=date, start_time=start_time, end_time=end_time,
                                                uname=uname, time_length=time_length)

            response = HttpResponseRedirect('index')
            response.set_cookie('cookie_end_time', end_time)
            return response

        if 'cancel' in req.POST:
            response = HttpResponseRedirect("login")
            response.delete_cookie('cookie_start_time')
            response.delete_cookie('cookie_end_time')
            return response
        if 'submit' in req.POST:
            reason = req.POST.get("reason")
            leave_time = req.POST.get("leave_time")
            time_add = DailyTime.objects.create(id=curtime, date=date, reason=reason, leave_time=leave_time,
                                                uname=uname, time_length=leave_time)
            return HttpResponseRedirect("index")

    return render(req, 'index.html', {'uname': uname, 'start_time': req.COOKIES.get('cookie_start_time', ''),
                                      'end_time': req.COOKIES.get('cookie_end_time', ''), 'date': date})


def attendance_check(req):
    uname = req.COOKIES.get('cookie_uname', '')
    Method = req.method

    if Method == 'POST':
        if 'day' in req.POST:
            day_check = connection.cursor()
            day_query = "select uname,start_time,end_time,CONCAT(FLOOR(time_length/3600),'时',FLOOR((time_length%3600)/60), '分',((time_length%3600)%60), '秒'),date from daily_time where to_days(date) = to_days(now())"
            day_check.execute(day_query)
            day_row = day_check.fetchall()  # ((1,2),(1,1))
            day_query1 = "select time_length from daily_time where to_days(date) = to_days(now())"
            day_check.execute(day_query1)
            day_row1 = day_check.fetchall()  # ((1,),(1,))
            day_row_list = list(day_row)  # [(1,2),(1,1)]

            for i in range(len(day_row1)):
                if int(day_row1[i][0]) >= 36000:
                    day_row1_list = list(day_row[i])
                    day_row1_list.append('<a href="#"><i class="fa fa-check text-navy"></i></a>')
                    day_row_list[i] = tuple(day_row1_list)

                else:
                    day_row1_list = list(day_row[i])
                    day_row1_list.append('<a href="#"><i class="fa fa-times hongse"></i></a>')
                    day_row_list[i] = tuple(day_row1_list)

            row_tuple = tuple(day_row_list)
        if 'week' in req.POST:
            week_check = connection.cursor()
            week_query = "select uname,start_time,end_time,CONCAT(FLOOR(time_length/3600),'时',FLOOR((time_length%3600)/60), '分',((time_length%3600)%60), '秒'),date from daily_time where date between current_date()-7 and sysdate()"
            week_check.execute(week_query)
            week_row = week_check.fetchall()  # ((1,2),(1,1))
            week_query1 = "select time_length from daily_time where date between current_date()-7 and sysdate()"
            week_check.execute(week_query1)
            week_row1 = week_check.fetchall()  # ((1,),(1,))
            week_row_list = list(week_row)  # [(1,2),(1,1)]

            for i in range(len(week_row1)):
                if int(week_row1[i][0]) >= 36000:
                    week_row1_list = list(week_row[i])
                    week_row1_list.append('<a href="#"><i class="fa fa-check text-navy"></i></a>')
                    week_row_list[i] = tuple(week_row1_list)

                else:
                    week_row1_list = list(week_row[i])
                    week_row1_list.append('<a href="#"><i class="fa fa-times hongse"></i></a>')
                    week_row_list[i] = tuple(week_row1_list)

            row_tuple = tuple(week_row_list)
        if 'month' in req.POST:
            month_check = connection.cursor()
            month_query = "select uname,start_time,end_time,CONCAT(FLOOR(time_length/3600),'时',FLOOR((time_length%3600)/60), '分',((time_length%3600)%60), '秒'),date from daily_time where DATE_FORMAT(date, '%Y%m' ) = DATE_FORMAT( CURDATE( ) , '%Y%m' )"
            month_check.execute(month_query)
            month_row = month_check.fetchall()  # ((1,2),(1,1))
            month_query1 = "select time_length from daily_time where DATE_FORMAT( date, '%Y%m' ) = DATE_FORMAT( CURDATE( ) , '%Y%m' )"
            month_check.execute(month_query1)
            month_row1 = month_check.fetchall()  # ((1,),(1,))
            month_row_list = list(month_row)  # [(1,2),(1,1)]

            for i in range(len(month_row1)):
                if int(month_row1[i][0]) >= 36000:
                    month_row1_list = list(month_row[i])
                    month_row1_list.append('<a href="#"><i class="fa fa-check text-navy"></i></a>')
                    month_row_list[i] = tuple(month_row1_list)

                else:
                    month_row1_list = list(month_row[i])
                    month_row1_list.append('<a href="#"><i class="fa fa-times hongse"></i></a>')
                    month_row_list[i] = tuple(month_row1_list)

            row_tuple = tuple(month_row_list)
    return render(req, 'monthqiandao.html', locals())