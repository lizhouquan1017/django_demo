# coding:utf-8
from utils import sqlheper
from django.shortcuts import render, redirect, HttpResponse
import json


def classse(request):
    class_list = sqlheper.get_list('select id,class_name from t_class', [])
    return render(request, 'classes.html', {'class_list': class_list})


def add_class(request):
    if request.method == 'GET':
        return render(request, 'add_class.html')
    else:
        print(request.POST)
        value = request.POST.get('class_name')
        if len(value) > 0:
            sqlheper.modify("insert into t_class(class_name) values(%s)", [value, ])
            return redirect('/classes/')
        else:
            return render(request, 'add_class.html', {'msg': '班级名称不能为空'})


def del_class(request):
    nid = request.GET.get('nid')
    sqlheper.modify("delete from t_class where id=%s", [nid, ])
    return redirect('/classes/')


def edit_class(request):
    if request.method == "GET":
        nid = request.GET.get('nid')
        result = sqlheper.get_one("select id,class_name from t_class where id = %s", [nid, ])
        print(result)
        return render(request, 'edit_class.html', {'result': result})
    else:
        nid = request.GET.get('nid')
        class_name = request.POST.get('class_name')
        sqlheper.modify("update t_class set class_name=%s where id = %s", [class_name, nid, ])
        return redirect('/classes/')


def modal_add_class(request):
    class_name = request.POST.get('class_name')
    if len(class_name) > 0:
        sqlheper.modify('insert into t_class(class_name) values(%s)', [class_name, ])
        return HttpResponse('ok')
    else:
        return HttpResponse('班级标题不能为空')


def modal_edit_class(request):
    ret = {'status': True, 'message':None}
    try:
        nid = request.POST.get('nid')
        content = request.POST.get('content')
        print(nid)
        print(content)
        sqlheper.modify('update t_class set class_name=%s where id=%s', [content, nid, ])
    except Exception as e:
        ret['status'] = False
        ret['message'] = "处理异常"
    return HttpResponse(json.dumps(ret))


def students(request):
    student_list = sqlheper.get_list('SELECT t_student.id,t_student.student_name,t_class.class_name from t_student '
                                     'LEFT JOIN  t_class on  t_student.class_id = t_class.id', [])
    class_list = sqlheper.get_list('select id,class_name from t_class', [])
    return render(request, 'students.html', {'class_list': class_list, 'student_list': student_list})


def add_student(request):
    if request.method == 'GET':
        class_list = sqlheper.get_list('select id,class_name from t_class', [])
        return render(request, 'add_student.html', {'class_list': class_list})
    else:
        print(request.POST)
        c_id = request.POST.get('class_id')
        value = request.POST.get('student_name')
        if len(value) > 0:
            sqlheper.modify("insert into t_student(student_name,class_id) values(%s,%s)", [value, c_id,])
            return redirect('/students/')
        else:
            return render(request, 'add_student.html', {'msg': '学生名称不能为空'})


def del_student(request):
    nid = request.GET.get('nid')
    sqlheper.modify("delete from t_student where id=%s", [nid, ])
    return redirect('/students/')


def edit_student(request):
    if request.method == "GET":
        nid = request.GET.get('nid')
        class_list = sqlheper.get_list("select id,class_name from t_class", [])
        print(class_list)
        current_sutdent_info = sqlheper.get_one("select id,student_name,class_id from t_student where id = %s", [nid, ])
        print(current_sutdent_info)
        return render(request, 'edit_studemt.html', {'class_list': class_list, 'current_sutdent_info': current_sutdent_info})
    else:
        nid = request.GET.get('nid')
        student_name = request.POST.get('student_name')
        sqlheper.modify("update t_student set student_name=%s where id = %s", [student_name, nid, ])
        return redirect('/students/')


def modal_add_student(request):
    student_name = request.POST.get('student_name')
    class_id = request.POST.get('class_id')
    if len(student_name) > 0:
        sqlheper.modify('insert into t_student(student_name,class_id) values(%s,%s)', [student_name, class_id, ])
        return HttpResponse('ok')
    else:
        return HttpResponse('学生名称不能为空')


def modal_edit_student(request):
    ret = {'status': True, 'message': None}
    try:
        nid = request.POST.get('nid')
        studnet_name = request.POST.get('studnet_name')
        class_id = request.POST.get('class_id')
        print(nid)
        print(studnet_name)
        print(class_id)
        sqlheper.modify('update t_student set student_name=%s ,class_id = %s where id=%s', [studnet_name, class_id, nid,])
    except Exception as e:
        ret['status'] = False
        ret['message'] = "处理异常"
    return HttpResponse(json.dumps(ret))

