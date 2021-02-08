from django.shortcuts import render
from . import models
from django.shortcuts import HttpResponseRedirect, Http404, HttpResponse, render
import json
import pdb
import csv
import codecs
from django.http import JsonResponse
from django.core import serializers
from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime
import numpy
from supervisor.excelimport import to_tableuser,to_tableorg
import xlrd
import os,time


# Create your views here.
def institute(request):
    user_name = request.session['user_name']
    o = models.TableOrganization.objects.all()
    if o.exists():
        _data = [
            {
                'id': x.table_organization_col_id,
                'name': x.table_organization_col_name,
                'pId': x.table_organization_col_parent_name.table_organization_col_id if x.table_organization_col_parent_name else 0,
                'open': 1,
            } for x in o
        ]
        n=0
        tmp=[]
        for i in range(len(_data)):
            if _data[i]['pId']==0:
                rootid=_data[i]['id']
                root=_data[i]
            if _data[i]['pId'] == rootid:
                n+=1
                tmp.append(_data[i])
        tree=[[]for i in range(n)]
        for i in range (n):
            tree[i].append(tmp[i])
        for each in _data:
            for i in range(n):
                for j in range(len(tree[i])):
                    if each['pId']==tree[i][j]['id']:
                        tree[i].append(each)
        # for each in tree:
        #     print(each['pId'])
        li=[]
        for i in range(len(tree)):
            li.append(i+1)
        # print(li)
        list = []
        eval_org = models.TableEvaluation.objects.values_list('table_evaluation_col_organization')
        for i in range(0, len(eval_org)):
            list.append(eval_org[i][0])
        listforfilter = json.dumps(list)
        # print(listforfilter)
        return render(request, 'supervisor/institute.html', {'data': _data, 'array': listforfilter,'user_name':user_name,'rooty':root,'tree':tree,'li':li,
                                                             'length':len(tree),'root':rootid})
    else:
        models.TableOrganization.objects.create(table_organization_col_name='机构树',
                                                table_organization_col_address=None,
                                                table_organization_col_postcode=None,
                                                table_organization_col_field=None,
                                                table_organization_col_parent_name=None)
        root = models.TableOrganization.objects.all()
        _data = [
            {
                'id': x.table_organization_col_id,
                'name': x.table_organization_col_name,
                'pId': x.table_organization_col_parent_name.table_organization_col_id if x.table_organization_col_parent_name else 0,
                'open': 1,
            } for x in root
        ]
        list = []
        eval_org = models.TableEvaluation.objects.values_list('table_evaluation_col_organization')
        for i in range(0, len(eval_org)):
            list.append(eval_org[i][0])
        listforfilter = json.dumps(list)
        return render(request, 'supervisor/institute.html', {'data': _data, 'array': listforfilter})


def organization_create(request):
    if request.method == 'POST':
        organization_name = request.POST.get('create_name')
        organization_code = request.POST.get('create_code')
        organization_location = request.POST.get('create_location')
        organization_zipcode = request.POST.get('create_zipcode')
        parent = models.TableOrganization.objects.get(table_organization_col_name=request.POST.get('parent_name'))
        organization_field = request.POST.get('create_field')
        org = models.TableOrganization.objects.filter(table_organization_col_name=organization_name)
        # pdb.set_trace()
        if org.exists():
            message = '该机构名已存在，请重新输入'
            return JsonResponse({'message': message})
        else:
            try:
                models.TableOrganization.objects.create(table_organization_col_name=organization_name,
                                                        table_organization_col_address=organization_location,
                                                        table_organization_col_postcode=organization_zipcode,
                                                        table_organization_col_field=organization_field,
                                                        table_organization_col_parent_name=parent,
                                                        table_organization_col_code=organization_code)
                return JsonResponse({'state': 1, 'message': '创建成功!'})
            except Exception as e:
                return JsonResponse({'state': 0, 'message': 'Create Error: ' + str(e)})


def organization_edit(request):
    if request.method == 'GET':
        organization_id = request.GET.get('edit_id')

        parent_id = request.GET.get('parent_id')
        org = serializers.serialize("json",
                                    models.TableOrganization.objects.filter(table_organization_col_id=organization_id))
        parent = models.TableOrganization.objects.filter(table_organization_col_id=parent_id).values_list(
            'table_organization_col_name')[0][0]

        return JsonResponse({'org': org, 'parent': parent})
    elif request.method == 'POST':
        organization_id = request.POST.get('edit_id')
        organization_name = request.POST.get('edit_name')
        organization_location = request.POST.get('edit_location')
        organization_zipcode = request.POST.get('edit_zipcode')
        organization_code=request.POST.get('edit_code')

        try:
            parent = models.TableOrganization.objects.get(
                table_organization_col_name=request.POST.get('edit_parent'))
        except:
            message = '父机构名不存在，请重新输入'
            return JsonResponse({'message': message})
            # 添加判断是否存在这个父节点
        # pdb.set_trace()
        organization_field = request.POST.get('edit_field')
        org = models.TableOrganization.objects.filter(table_organization_col_name=organization_name)
        if org.exists() and str(org.values_list('table_organization_col_id')[0][0]) != organization_id:
            message = '该机构名已存在，请重新输入'
            return JsonResponse({'message': message})
        try:
            models.TableOrganization.objects.filter(table_organization_col_id=organization_id).update(
                table_organization_col_name=organization_name,
                table_organization_col_address=organization_location,
                table_organization_col_postcode=organization_zipcode,
                table_organization_col_field=organization_field,
                table_organization_col_parent_name=parent,
                table_organization_col_code=organization_code
            )
            return JsonResponse({'state': 1, 'message': '修改成功!'})
        except Exception as e:
            return JsonResponse({'state': 0, 'message': 'Edit Error: ' + str(e)})


def organization_delete(request):
    if request.method == 'POST':
        organization_id = request.POST.get('delete_id')
        try:
            models.TableOrganization.objects.get(table_organization_col_id=organization_id).delete()
            return JsonResponse({'state': 1, 'message': '修改成功!'})
        except Exception as e:
            return JsonResponse({'state': 0, 'message': 'Edit Error: ' + str(e)})


def organization_export(request):
    # pdb.set_trace()
    response = HttpResponse(content_type='text/csv')
    response.write(codecs.BOM_UTF8)
    response['Content-Disposition'] = "attachment;filename=organization.csv"
    writer = csv.writer(response)
    org_csv = models.TableOrganization.objects.filter(~Q(table_organization_col_name='机构列表'))
    writer.writerow(['Org_Name','Org_Code','Org_Address','Org_Post','Org_Field','Org_Parent_Name'])
    write_length= len(org_csv)
    write_position=0
    while write_position < write_length:
        try:
            org_row = org_csv[write_position]
            parent_org_query = org_row.table_organization_col_parent_name
            parent_org = parent_org_query.table_organization_col_name
            if parent_org == '机构列表':
                try:
                    writer.writerow([org_row.table_organization_col_name,org_row.table_organization_col_code,
                                     org_row.table_organization_col_address, org_row.table_organization_col_postcode,
                                     org_row.table_organization_col_field,org_row.table_organization_col_parent_name_id])
                    write_position += 1
                except:
                    return JsonResponse({'message':'根问题'})
            else:
                try:
                    writer.writerow([org_row.table_organization_col_name,org_row.table_organization_col_code,
                                     org_row.table_organization_col_address, org_row.table_organization_col_postcode,
                                     org_row.table_organization_col_field,org_row.table_organization_col_parent_name_id])
                    write_position += 1
                except:
                    return JsonResponse({'message':'下级机构问题'})
        except:
            return JsonResponse({'message':'检查父级机构'})
    return response


def user_delete(request):
    # pdb.set_trace()
    if request.method == 'POST':
        user_id = request.POST.get('delete_id')
        # userobj = models.TableUser.objects.filter(table_user_col_id=user_id)
        # objname = userobj.values_list('table_user_col_real_name')[0][0]
        # if models.TableEvaluation.objects.

        for user_del in models.TableUser.objects.filter(table_user_col_id=user_id):
            real_name_del = user_del.table_user_col_real_name
            list_admin = []
        for eval_sys in models.TableEvaluation.objects.all():
            list_admin.append(eval_sys.table_evaluation_col_administrator)

        if real_name_del in list_admin:
            return JsonResponse({'state': 0, 'message': '用户使用中，禁止删除'})

        else:
            try:
                models.TableUser.objects.get(table_user_col_id=user_id).delete()
                return JsonResponse({'state': 1, 'message': '修改成功!'})
            except Exception as e:
                return JsonResponse({'state': 0, 'message': 'Edit Error: ' + str(e)})


def user_edit(request):
    if request.method == 'GET':
        ppl_id = request.GET.get('edit_id')
        ppl = serializers.serialize("json",
                                    models.TableUser.objects.filter(table_user_col_id=ppl_id))
        # print(ppl)
        return JsonResponse({'ppl': ppl})
    elif request.method == 'POST':
        # pdb.set_trace()
        user_id = request.POST.get('edit_id')
        user_name = request.POST.get('edit_name')
        user_realname = request.POST.get('edit_realname')
        user_sex = request.POST.get('edit_sex')
        user_password = request.POST.get('edit_password')
        user_password_twice = request.POST.get('edit_password_twice')
        user_organization = request.POST.get('edit_organization')
        user_organizationID = models.TableOrganization.objects.get(
            table_organization_col_name=user_organization)
        user_department = request.POST.get('edit_department'),
        user_title = request.POST.get('edit_title'),
        user_field = request.POST.get('edit_field'),
        user_email = request.POST.get('edit_email'),
        user_edu = request.POST.get('edit_edu')
        user_memo = request.POST.get('edit_memo')
        user_identity = request.POST.get('edit_identity')
        user_type = request.POST.get('edit_type')
        if user_type == '超级管理员':
            user_type_id = 0
        elif user_type == '管理员':
            user_type_id = 1
        elif user_type == '审核':
            user_type_id = 2
        elif user_type == '机构用户':
            user_type_id = 3
        elif user_type == '专家用户':
            user_type_id = 4
        else:
            user_type_id = None

        user_mobilenumber = request.POST.get('edit_mobilenumber')
        user_telnumber = request.POST.get('edit_telnumber')
        username = models.TableUser.objects.filter(table_user_col_name=user_name)
        print(type(username))
        if username.exists() and str(username.values_list('table_user_col_id')[0][0]) != user_id:
            message = '该用户名已存在，请重新输入'
            return JsonResponse({'message': message})
        useremail = models.TableUser.objects.filter(table_user_col_email=user_email)
        if useremail.exists() and str(useremail.values_list('table_user_col_id')[0][0]) != user_id:
            message = '该邮箱以被使用，请重新输入'
            return JsonResponse({'message': message})
        usermobile = models.TableUser.objects.filter(table_user_col_mobile=user_mobilenumber)
        if usermobile.exists() and str(usermobile.values_list('table_user_col_id')[0][0]) != user_id:
            message = '该手机号以被使用，请重新输入'
            return JsonResponse({'message': message})
        if user_password != user_password_twice:
            message = '你两次输入的密码不一致，请重新输入'
            return JsonResponse({'message': message})
        try:
            models.TableUser.objects.filter(table_user_col_id=user_id).update(table_user_col_name=user_name,
                                                                              table_user_col_real_name=user_realname,
                                                                              table_user_col_sex=user_sex,
                                                                              table_user_col_type=user_type,
                                                                              table_user_col_type_id=user_type_id,
                                                                              table_user_col_password=make_password(
                                                                                  user_password),
                                                                              table_user_col_organization=
                                                                              user_organizationID,
                                                                              table_user_col_department=user_department[
                                                                                  0],
                                                                              table_user_col_title=user_title[0],
                                                                              table_user_col_work_field=user_field[0],
                                                                              table_user_col_email=user_email[0],
                                                                              table_user_col_bachelor=user_edu,
                                                                              table_user_col_mobile=user_mobilenumber,
                                                                              table_user_col_tel=user_telnumber,
                                                                              table_user_col_memo=user_memo,
                                                                              table_user_col_IdentityID=user_identity
                                                                              )

            return JsonResponse({'state': 1, 'message': '修改成功!'})
        except Exception as e:
            return JsonResponse({'state': 0, 'message': 'Create Error: ' + str(e)})


def user_create(request):
    global user_type_id
    if request.method == 'POST':
        user_name = request.POST.get('create_name')
        user_realname = request.POST.get('create_realname')
        user_sex = request.POST.get('create_sex')
        user_password = request.POST.get('create_password')
        user_password_twice = request.POST.get('create_password_twice')
        user_organization = request.POST.get('create_organization')
        user_organizationID = models.TableOrganization.objects.get(
            table_organization_col_name=user_organization)
        user_department = request.POST.get('create_department'),
        user_title = request.POST.get('create_title'),
        user_field = request.POST.get('create_field'),
        user_email = request.POST.get('create_email'),
        user_edu = request.POST.get('create_edu')
        user_memo = request.POST.get('create_memo')
        user_identity = request.POST.get('create_identity')
        user_type = request.POST.get('create_type')
        if user_type == '超级管理员':
            user_type_id = 0
        elif user_type == '管理员':
            user_type_id = 1
        elif user_type == '审核':
            user_type_id = 2
        elif user_type == '机构用户':
            user_type_id = 3
        elif user_type == '专家用户':
            user_type_id = 4
        else:
            user_type = None
        user_mobilenumber = request.POST.get('create_mobilenumber')
        user_telnumber = request.POST.get('create_telnumber')
        username = models.TableUser.objects.filter(table_user_col_name=user_name)
        if username.exists():
            message = '该用户名已存在，请重新输入'
            print(message)
            return JsonResponse({'message': message})
        useremail = models.TableUser.objects.filter(table_user_col_email=user_email)
        if useremail.exists():
            message = '该邮箱以被使用，请重新输入'
            return JsonResponse({'message': message})
        usermobile = models.TableUser.objects.filter(table_user_col_mobile=user_mobilenumber)
        if usermobile.exists():
            message = '该手机号以被使用，请重新输入'
            return JsonResponse({'message': message})
        if user_password != user_password_twice:
            message = '你两次输入的密码不一致，请重新输入'
            return JsonResponse({'message': message})
        try:
            models.TableUser.objects.create(
                                            table_user_col_name=user_name,
                                            table_user_col_real_name=user_realname,
                                            table_user_col_sex=user_sex,
                                            table_user_col_type=user_type,
                                            table_user_col_type_id=user_type_id,
                                            table_user_col_password=make_password(
                                                user_password),
                                            table_user_col_organization=
                                            user_organizationID,
                                            table_user_col_department=user_department[
                                                0],
                                            table_user_col_title=user_title[0],
                                            table_user_col_work_field=user_field[0],
                                            table_user_col_email=user_email[0],
                                            table_user_col_bachelor=user_edu,
                                            table_user_col_mobile=user_mobilenumber,
                                            table_user_col_tel=user_telnumber,
                                            table_user_col_memo=user_memo,
                                            table_user_col_IdentityID=user_identity
                                            ),
            return JsonResponse({'state': 1, 'message': '创建成功!'})
        except Exception as e:
            return JsonResponse({'state': 0, 'message': 'Create Error: ' + str(e)})


def people(request):
    user_name = request.session['user_name']
    users = models.TableUser.objects.all()
    organization = models.TableOrganization.objects.filter(~Q(table_organization_col_name="机构列表"))
    return render(request, 'supervisor/people.html', locals())


def organization_evaluation(request):
    user_name = request.session['user_name']
    org_eval = models.TableEvaluation.objects.all()
    organizations = models.TableOrganization.objects.filter(~Q(table_organization_col_name="机构树"))
    users = models.TableUser.objects.filter(table_user_col_type_id=1)
    return render(request, 'supervisor/evaluation.html', locals())


def evaluation_create(request):
    if request.method == 'POST':
        # pdb.set_trace()
        evalutaion_name = request.POST.get('name')
        evaluation_admin = request.POST.get('admin')
        evaluation_status = request.POST.get('status')
        evaluation_createtime = request.POST.get('createtime')
        evaluation_endtime = request.POST.get('endtime')
        evaluation_deliver = request.POST.get('deliver')
        evaluation_mark = request.POST.get('mark')
        evalutaion_organization = request.POST.get('organization')
        try:
            models.TableEvaluation.objects.create(table_evaluation_col_name=evalutaion_name,
                                                  table_evaluation_col_administrator=evaluation_admin,
                                                  table_evaluation_col_status=evaluation_status,
                                                  table_evaluation_col_create_time=evaluation_createtime,
                                                  table_evaluation_col_finish_time=evaluation_endtime,
                                                  table_evaluation_col_organization=evalutaion_organization,
                                                  table_evaluation_col_deliver=evaluation_deliver,
                                                  table_evaluation_col_mark=evaluation_mark)
            return JsonResponse({'state': 1, 'message': '创建成功!'})
        except Exception as e:
            return JsonResponse({'state': 0, 'message': 'Create Error: ' + str(e)})


def evaluation_edit(request):
    if request.method == 'GET':
        evaluation_id = request.GET.get('edit_id')
        eva = serializers.serialize("json",
                                    models.TableEvaluation.objects.filter(table_evaluation_col_id=evaluation_id))
        print(eva)
        return JsonResponse({'eva': eva})
    elif request.method == 'POST':
        # pdb.set_trace()
        evaluation_id = request.POST.get('edit_id')
        evalutaion_name = request.POST.get('name')
        evaluation_admin = request.POST.get('admin')
        evaluation_status = request.POST.get('status')
        evaluation_createtime = request.POST.get('createtime')
        evaluation_endtime = request.POST.get('endtime')
        evaluation_deliver = request.POST.get('deliver')
        evaluation_mark = request.POST.get('mark')
        evalutaion_organization = request.POST.get('organization')
        if evaluation_endtime > evaluation_createtime:
            try:
                models.TableEvaluation.objects.filter(table_evaluation_col_id=evaluation_id).update(
                    table_evaluation_col_name=evalutaion_name,
                    table_evaluation_col_administrator=evaluation_admin,
                    table_evaluation_col_status=evaluation_status,
                    table_evaluation_col_create_time=evaluation_createtime,
                    table_evaluation_col_finish_time=evaluation_endtime,
                    table_evaluation_col_organization=evalutaion_organization,
                    table_evaluation_col_deliver=evaluation_deliver,
                    table_evaluation_col_mark=evaluation_mark)
                return JsonResponse({'state': 1, 'message': '创建成功!'})
            except Exception as e:
                return JsonResponse({'state': 0, 'message': 'Create Error: ' + str(e)})
        else:
            return JsonResponse({'message':'截止时间不得早于开始时间！'})

def evaluation_delete(request):
    if request.method == 'POST':
        evaluation_id = request.POST.get('delete_id')
        for eval_del in models.TableEvaluation.objects.filter(table_evaluation_col_id=evaluation_id):
            if eval_del.table_evaluation_col_status == '启用':
                return JsonResponse({'state': 0, 'message': '项目已启动，无法删除 '})
            else:
                try:
                    models.TableEvaluation.objects.get(table_evaluation_col_id=evaluation_id).delete()
                    return JsonResponse({'state': 1, 'message': '删除成功!'})
                except Exception as e:
                    return JsonResponse({'state': 0, 'message': 'Edit Error: ' + str(e)})


## Import Excel
# 读取excel表格
def excel_import_user(filename):
    # pdb.set_trace()
    file_excel = 'C:/Users/Administrator/Desktop/DESP-qzc/DESP/uploads/indicator/' + str(filename)
    # print(file_excel)
    col_name_index = 0
    by_name = u'Sheet1'
    data = xlrd.open_workbook(file_excel)  # 打开excel
    table = data.sheet_by_name(by_name)  # 表单名称
    n_rows = table.nrows  # 行数
    row_dict = {}
    # try:
    for row_num in range(1, n_rows):
            row = table.row_values(row_num)  # 获得每行的字段
            # seq = [row[0], row[1], row[2], row[3]]
            seq_user = {'User_Type': row[0], 'User_Username': row[1],
                        'User_Real_Name': row[2], 'User_Org': row[3], 'User_Mobile': row[4], 'User_Tel': row[5],
                        'User_Password': make_password(str(row[6])), 'User_Email': row[7], 'User_Title': row[8],
                        'User_Department': row[9], 'User_Work_Field': row[10], 'User_Sex': row[11],
                        'User_Bachelor': row[12], 'User_Memo': row[13], 'User_Identity': row[14]}
            row_dict[row_num] = seq_user
    data_user = {
            'code': '200',
            'msg': 'success',
            'data': row_dict
        }
    user_write = data_user['data']
    max_position = len(user_write)
    # except:
    #     return JsonResponse({'message': '模板错误'})
    try:
        position = 1
        while position <= max_position:
            try:
                arrs = user_write[position]
                orgname = arrs['Org_Name']
                org_query = models.TableOrganization.objects.get(table_organization_col_name=orgname)
                # print(org_id)
            except:
                return JsonResponse({'message': '检查上级机构问题'})
            try:
                if arrs['Type'] == '超级管理员':
                    type_id = 0
                elif arrs['Type'] == '管理员':
                    type_id = 1
                elif arrs['Type'] == '审核':
                    type_id = 2
                elif arrs['Type'] == '机构用户':
                    type_id = 3
                elif arrs['Type'] == '专家用户':
                    type_id = 4
            except:
                return JsonResponse({'message': '用户类型问题'})
            try:
                models.TableUser.objects.create(table_user_col_type_id=type_id,
                                                table_user_col_type=arrs['User_Type'],
                                                table_user_col_name=arrs['User_Username'],
                                                table_user_col_real_name=arrs['User_Real_Name'],
                                                table_user_col_organization_id=org_query,
                                                table_user_col_mobile=arrs['User_Mobile'],
                                                table_user_col_tel=arrs['User_Tel'],
                                                table_user_col_password=arrs['User_Password'],
                                                table_user_col_email=arrs['User_Email'],
                                                table_user_col_title=arrs['User_Title'],
                                                table_user_col_department=arrs['User_Department'],
                                                table_user_col_work_field=arrs['User_Work_Field'],
                                                table_user_col_sex=arrs['User_Sex'],
                                                table_user_col_bachelor=arrs['User_Bachelor'],
                                                table_user_col_memo=arrs['User_Memo'],
                                                table_user_col_IdentityID=arrs['User_Identity'])
                position = position + 1
            except:
                return JsonResponse({'message': '检查填报内容'})
        else:
            return JsonResponse({'message': '上传成功'})
    except:
        return JsonResponse({'message': '检查填报内容'})

    # # 调用方法 ---自定义模板函数 这里必须要return
    # return to_tableuser(data_user)


def upload_user(request):
    # pdb.set_trace()
    if request.method == 'GET':
        return render(request, 'supervisor/people.html')
    elif request.method == 'POST':
        obj = request.FILES.get('file_obj')
        obj.name = time.strftime("%Y%m%d_%H_%M_%S_", time.localtime(time.time())) + obj.name
        # print(obj)
        if str(obj).endswith('.xlsx'):
            f = open(os.path.join('DESP', 'uploads', 'user', obj.name), 'wb')
            for chunk in obj.chunks():
                f.write(chunk)
            f.close()
            return excel_import_user(obj)
        else:
            return JsonResponse({'message': '文件格式错误！'})


def download_user(request):
    # pdb.set_trace()
    file = open('DESP/uploads/user/TableUser_Import.xlsx', 'rb')
    response = HttpResponse(file)
    response['Content-Type'] = 'application/octet-stream'  # 设置头信息，告诉浏览器这是个文件
    response['Content-Disposition'] = 'attachment;filename="TableUser_Import.xlsx"'
    return response

def user_export(request):
    response = HttpResponse(content_type='text/csv')
    response.write(codecs.BOM_UTF8)
    response['Content-Disposition'] = "attachment;filename=user_list.csv"
    writer = csv.writer(response)
    user_csv = models.TableUser.objects.all()
    writer.writerow(['User_Type', 'User_Username','User_Real_Name','User_Org','User_Mobile','User_Tel','User_Password',
                     'User_Email','User_Title','User_Department','User_Work_Field','User_Sex','User_Bachelor',
                     'User_Memo','User_Identity'])
    write_length= len(user_csv)
    write_position=0
    while write_position < write_length:
        try:
            user_row = user_csv[write_position]
            user_org_query = user_row.table_user_col_organization
            org_name=user_org_query.table_organization_col_name
        except:
            return JsonResponse({'message':'人员机构数据绑定问题'})
        try:
            writer.writerow([user_row.table_user_col_type, user_row.table_user_col_name,user_row.table_user_col_real_name,
                             org_name,user_row.table_user_col_mobile,user_row.table_user_col_tel,'不显示',
                             user_row.table_user_col_email,user_row.table_user_col_title,user_row.table_user_col_department,
                             user_row.table_user_col_work_field,user_row.table_user_col_sex,user_row.table_user_col_bachelor,
                             user_row.table_user_col_memo,user_row.table_user_col_IdentityID])
            write_position += 1
        except:
            return JsonResponse({'message':'录入问题'})
    return response

def excel_import_organization(filename):
    file_excel = 'DESP/uploads/organization/' + str(filename)  ##存储路径
    # print(file_excel)
    col_name_index = 0
    by_name = u'Sheet1'
    data = xlrd.open_workbook(file_excel)  # 打开excel
    table = data.sheet_by_name(by_name)  # 表单名称
    n_rows = table.nrows  # 行数
    row_dict = {}
    for row_num in range(1, n_rows):
            row = table.row_values(row_num)  # 获得每行的字段
            seq_org = {'Org_Name': row[0], 'Org_Address': row[1], 'Org_Post': str(row[2]),
                       'Org_Field': row[3], 'Org_Parent_Name': row[4], 'Org_Code': row[5]}
            try:
                orgNamecheck = models.TableOrganization.objects.filter(table_organization_col_name=seq_org['Org_Name'])
                orgCodecheck = models.TableOrganization.objects.filter(table_organization_col_code=seq_org['Org_Code'])
            except:
                returndata = {'message': '检查填报内容'}
                return returndata
            else:
                if orgCodecheck.exists():
                    print(str(seq_org['Org_Code']))
                    returndata = {'message': '编码 '+str(seq_org['Org_Code'])+' 已存在, 对应的单位名称是'+
                                  orgCodecheck[0].table_organization_col_name+', 请使用其它编码'}
                    return returndata
                elif orgNamecheck.exists():
                    print(str(seq_org['Org_Name']))
                    returndata = {'message': '单位名称: “'+str(seq_org['Org_Name'])+'” 已存在，请通过[修改机构]功能直接对该单位信息进行修改'}
                    return returndata
            row_dict[row_num] = seq_org
    data_org = {
            'code': '200',
            'msg': 'success',
            'data': row_dict
        }
    org_write = data_org['data']
    max_position = len(org_write)
        # print(max_position)

    try:
        position = 1
        while position <= max_position:
            try:
                arrs = org_write[position]
                # print(arrs)
                orgname = arrs['Org_Parent_Name']
                parent_id = models.TableOrganization.objects.get(table_organization_col_name=orgname)
                models.TableOrganization.objects.create(table_organization_col_name=arrs['Org_Name'],
                                                        table_organization_col_address=arrs['Org_Address'],
                                                        table_organization_col_postcode=arrs['Org_Post'],
                                                        table_organization_col_field=arrs['Org_Field'],
                                                        table_organization_col_parent_name=parent_id,
                                                        table_organization_col_code=arrs['Org_Code'])
                position = position + 1
            except:
                returndata={'message': '检查填报内容'}
                print(returndata)
                return returndata
    except:
        returndata={'message': '检查填报内容'}
        print(returndata)

        return returndata
    else:
        returndata = {'message': '上传成功'}
        print(returndata)
        return returndata

    # # 调用方法 ---自定义模板函数 这里必须要return
    # return to_tableorg(data_org)


def upload_organization(request):
    # pdb.set_trace()
    if request.method == 'GET':
        return render(request, 'supervisor/institute.html')
    elif request.method == 'POST':
        obj = request.FILES.get('file_obj_org')
        obj.name = time.strftime("%Y%m%d_%H_%M_%S_", time.localtime(time.time())) + obj.name
        # print(obj)
        if str(obj).endswith('.xlsx'):
            f = open(os.path.join('DESP', 'uploads', 'organization', obj.name), 'wb')  ##存储位置
            for chunk in obj.chunks():
                f.write(chunk)
            f.close()
            message=excel_import_organization(obj)
            os.remove(os.path.join('DESP', 'uploads', 'organization', obj.name))
            return JsonResponse(message)
        else:
            return JsonResponse({'message': '文件格式错误！'})


def download_organization(request):
    try:
        # pdb.set_trace()
        file = open('DESP/uploads/organization/TableOrg_Import.xlsx', 'rb')
        response = HttpResponse(file)
        response['Content-Type'] = 'application/octet-stream'  # 设置头信息，告诉浏览器这是个文件
        response['Content-Disposition'] = 'attachment;filename="TableOrg_Import.xlsx"'
    except:
        return HttpResponse("该文件不存在")
    return response


