import random
import string

import xlrd
from django.contrib.auth.hashers import make_password, check_password
from django.db import transaction
from django.shortcuts import redirect
from django.shortcuts import render
from django.views import View
from administrator.models import TableTimeliner, TableQuestionContent, TableQuestionResult
from login import models
from login.forms import ForgetForm, ResetForm
from login.utils.email_send import send_register_email
from supervisor.models import TableEvaluation
from supervisor.models import TableOrganization
from administrator.models import TableTimeliner
from . import forms
from . import models
import datetime
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
import xlwt
from io import BytesIO
from xlwt import Workbook
from django.utils.encoding import escape_uri_path
from .models import TableUser



# Create your views here.
def login(request):
    # pdb.set_trace()
    if request.session.get('is_login', None):  # 登录后再次进入login页面，则根据其权限进入对应页面

        if request.session.get('permission') == 0:
            return redirect('/supervisor')
        if request.session.get('permission') == 1:
            return redirect('/administrator')
        if request.session.get('permission') == 3:
            return redirect('/user')
        if request.session.get('permission') == 4:
            return redirect('/expert')
        if request.session.get('permission') == 2:
            return redirect('/manager')

    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            # remember_me = request.POST.get('remember_me')
            remember_me = login_form.cleaned_data.get('remember_me')
            try:
                user = models.TableUser.objects.get(table_user_col_name=username)
            except:

                try:
                    user = models.TableUser.objects.get(table_user_col_mobile=username)
                except:
                    try:
                        user = models.TableUser.objects.get(table_user_col_email=username)
                    except:
                        message = '用户名不存在！'
                        return render(request, 'login/login.html', locals())

            encryptpwd = user.table_user_col_password
            if check_password(password, encryptpwd) == True:

                request.session['is_login'] = True
                request.session['user_id'] = user.table_user_col_id
                request.session['user_name'] = user.table_user_col_name
                request.session['permission'] = user.table_user_col_type_id
                request.session['lastlogintime'] = datetime.datetime.now().timestamp()
                if not remember_me:
                    request.session.set_expiry(0)
                if user.table_user_col_type_id == 0:
                    return redirect('/supervisor')
                if user.table_user_col_type_id == 1:
                    return redirect('/administrator')
                if user.table_user_col_type_id == 3:
                    return redirect('/user')
                if user.table_user_col_type_id == 4:
                    return redirect('/expert')
                if user.table_user_col_type_id == 2:
                    return redirect('/manager')

            else:
                message = '密码错误，请重新输入'
                return render(request, 'login/login.html', locals())

        else:
            message = '输入有误，请重新输入'
            return render(request, 'login/login.html', locals())

    login_form = forms.UserForm()
    return render(request, 'login/login.html', locals())


def reset(request):
    user_name = request.session['user_name']
    if request.method == 'POST':
        user_password = request.POST.get('edit_password')
        user_password_twice = request.POST.get('edit_password_twice')
        if user_password != user_password_twice:
            message = '你两次输入的密码不一致，请重新输入'
            return JsonResponse({'message': message})
        try:
            models.TableUser.objects.filter(table_user_col_name=user_name).update(
                table_user_col_password=make_password(
                    user_password)
            )
            print(user_password)
            return JsonResponse({'state': 1, 'message': '修改成功!'})
        except Exception as e:
            print(e)
            return JsonResponse({'state': 0, 'message': 'Create Error: ' + str(e)})


def supervisor(request):
    # pdb.set_trace()
    user_name = request.session['user_name']
    if not request.session.get('is_login', None) or request.session['permission'] != 0:  # 没登录过的或权限不对的，都直接返回到登录界面
        return redirect('/')
    org_eval = TableEvaluation.objects.all()
    organizations = TableOrganization.objects.filter(~Q(table_organization_col_name="机构树"))
    o = TableOrganization.objects.all()
    if o.exists():
        data1 = [
            {
                'id': x.table_organization_col_id,
                'name': x.table_organization_col_name,
                'pId': x.table_organization_col_parent_name.table_organization_col_id if x.table_organization_col_parent_name else 0,
                'open': 1,
                'checked': 0
            } for x in o
        ]
    # print(type(data1))

    data_org = TableEvaluation.objects.all()
    # print(data_org[1].table_evaluation_col_id)
    evaindex = []
    for each in data_org:
        evaindex.append(each.table_evaluation_col_id)
    # print(evaindex)
    length = len(evaindex)
    # print(data_org)
    orgs = []
    inde = []
    name = ''
    for each in data_org:
        # print(each.table_evaluation_col_organization)
        for letter in each.table_evaluation_col_organization:
            i = 0
            # print(letter)
            if letter != ',':
                name += letter
            else:
                # print(name, '\n')
                inde.append(name)
                name = ''
            if len(name) == len(each.table_evaluation_col_organization):
                # print(name, '\n')
                inde.append(name)
                orgs.append(inde)
                inde = []
                name = ''
                i += 1
        if i == 0:
            orgs.append(inde)
            inde = []
            name = ''
    # print(orgs)

    p = TableOrganization.objects.all()
    index = 0
    data2 = []
    data2_a = []
    for x in orgs:
        for each in p:
            for each1 in x:
                # print(each.table_organization_col_id)
                if int(each1) == each.table_organization_col_id:
                    # print(each1)
                    index += 1
            if index == 0:
                data2.append({
                    'id': each.table_organization_col_id,
                    'name': each.table_organization_col_name,
                    'pId': each.table_organization_col_parent_name.table_organization_col_id if each.table_organization_col_parent_name else 0,
                    'open': 1,
                    'checked': 0
                })
            else:
                data2.append({
                    'id': each.table_organization_col_id,
                    'name': each.table_organization_col_name,
                    'pId': each.table_organization_col_parent_name.table_organization_col_id if each.table_organization_col_parent_name else 0,
                    'open': 1,
                    'checked': 1
                })
                index = 0
        # print(data2)
        data2_a.append(data2)
        data2 = []
    # print(data2_a[9])
    # rett=data2_a[3]

    users = models.TableUser.objects.filter(table_user_col_type_id=1)
    return render(request, 'supervisor/evaluation.html', locals())


def administrator(request):
    if not request.session.get('is_login', None) or request.session['permission'] != 1:
        return redirect('/')
    str = request.session.get('lastlogintime')
    d = datetime.datetime.fromtimestamp(str)
    lastlogintime = d.strftime("%Y-%m-%d %H:%M:%S.%f")
    username = request.session.get('user_name')
    models.TableUser.objects.filter(table_user_col_name=username).update(table_user_col_lastlogintime=lastlogintime)
    timeevalname = TableTimeliner.objects.values('table_timeliner_col_evaluation').distinct().order_by(
        'table_timeliner_col_evaluation')
    administrator = request.session['user_name']
    timeline_list = TableTimeliner.objects.all()
    evalname = TableEvaluation.objects.filter(
        Q(table_evaluation_col_administrator=administrator))  # & Q(table_evaluation_col_status='启用'))
    eval_data = [
        {
            # 'org_id': TableOrganization.objects.filter(
            #     Q(table_organization_col_name=project.table_evaluation_col_organization)).values_list(
            #     'table_organization_col_id')[0][0],
            # 'org_name': project.table_evaluation_col_organization,
            'project_name': project.table_evaluation_col_name,
            'project_admin': project.table_evaluation_col_administrator,
            'questionaire_status': project.table_evaluation_col_status,
            'enddate': project.table_evaluation_col_finish_time,
        } for project in evalname
    ]
    return render(request, 'login/administrator.html',
                  {'eval_data': eval_data, 'evalname': evalname, 'admin': administrator})


def user(request):
    if not request.session.get('is_login', None) or request.session['permission'] != 3:
        return redirect('/')
    user_name = request.session['user_name']
    print(user_name)
    orgid = \
        models.TableUser.objects.filter(table_user_col_name=user_name).values_list('table_user_col_organization')[0][0]
    orgname = \
        TableOrganization.objects.filter(table_organization_col_id=orgid).values_list('table_organization_col_name')[0][
            0]
    print(orgid, orgname)
    data_org = TableEvaluation.objects.all()
    evaindex = []
    for each in data_org:
        evaindex.append(each.table_evaluation_col_id)
    orgs = []
    inde = []
    name = ''
    for each in data_org:
        print(each)
        for letter in each.table_evaluation_col_organization:
            i = 0
            if letter != ',':
                name += letter
            else:
                inde.append(name)
                name = ''
            if len(name) == len(each.table_evaluation_col_organization):
                inde.append(name)
                orgs.append(inde)
                inde = []
                name = ''
                i += 1
        if i == 0:
            orgs.append(inde)
            inde = []
            name = ''
    i = 0
    count = 0
    listeval = []
    for x in orgs:
        index = 0
        # print(x)
        for each1 in x:
            if int(each1) == orgid:
                index += 1
        if index == 0:
            i += 1
        else:
            t = i + count
            eval = TableEvaluation.objects.filter(table_evaluation_col_id=evaindex[t])
            listeval.append(eval)
            count += 1

    evals = []
    for each in listeval:
        evals.append(each[0].table_evaluation_col_name)
    print(listeval)
    name1 = request.GET.get('name1')
    if len(evals)==0:
        return render(request, 'login/usrselect.html', {'user': user_name, 'orgname': orgname})
    for each in evals:
        if len(each) != 0:
            eval_id = TableEvaluation.objects.get(table_evaluation_col_name=evals[0])
            questionaire_answer = set(
                TableQuestionContent.objects.filter(
                    table_question_content_col_evalname_id=eval_id).values_list(
                    'table_question_content_col_indicator_id'))
            group = []
            for eachquestion in questionaire_answer:
                group.append(eachquestion)
            list = []
            for i in range(0, len(questionaire_answer)):
                list.append(TableQuestionContent.objects.filter(table_question_content_col_indicator_id=group[i][0]))
            if len(list) != 0:
                page = request.GET.get('page')
                question = []
                if page == None:
                    for x in list[0]:
                        question.append({
                            'question_id': x.table_question_content_col_question_id,
                            'question_type': x.table_question_content_col_question_type,
                            'content': x.table_question_content_col_content,
                            'indicator_id': x.table_question_content_col_indicator_id,
                            'question_class': x.table_question_content_col_question_class,
                        })
                    page_num = 0
                else:
                    num = int(page)
                    for x in list[num]:
                        question.append({
                            'question_id': x.table_question_content_col_question_id,
                            'question_type': x.table_question_content_col_question_type,
                            'content': x.table_question_content_col_content,
                            'indicator_id': x.table_question_content_col_indicator_id,
                            'question_class': x.table_question_content_col_question_class,
                        })
                    page_num = num
                return render(request, 'login/usrselect.html',
                              {'names': evals, 'l': len(evals),
                               'user': user_name, 'orgname': orgname, })

            else:
                return render(request, 'login/usrselect.html', {'names': evals, 'user': user_name, 'orgname': orgname})
        else:
            return render(request, 'login/usrselect.html', {'names': evals, 'user': user_name, 'orgname': orgname})


def expert(request):
    if not request.session.get('is_login', None) or request.session['permission'] != 4:
        return redirect('/')
    administrator = request.session['user_name']

    return render(request, 'expert/expert.html', {'user_name': administrator})


def manager(request):
    if not request.session.get('is_login', None) or request.session['permission'] != 2:
        return redirect('/')
    administrator = request.session['user_name']
    print(administrator)
    evalname = TableEvaluation.objects.all().values('table_evaluation_col_name')
    timeevalname = TableTimeliner.objects.values('table_timeliner_col_evaluation').distinct().order_by(
        'table_timeliner_col_evaluation')
    # print(timeevalname)
    timeline_list = TableTimeliner.objects.filter(
        table_timeliner_col_evaluation=request.GET.get('timeevalname')).order_by('table_timeliner_col_start')
    dateline_list = TableTimeliner.objects.filter(
        table_timeliner_col_evaluation=request.GET.get('timeevalname')).order_by('table_timeliner_col_start')
    date_length = len(dateline_list)
    order_list = []
    order_count = 0
    while order_count < date_length:
        order_list.append(dateline_list.values_list('table_timeliner_col_id')[order_count][0])
        order_count = order_count + 1
    dateline = TableTimeliner.objects.filter(pk__in=order_list)
    for date in dateline:
        date_start = date.table_timeliner_col_start
        date_new_start = str(date_start).replace('-', '/')
        date_use_start = date_new_start[-2:] + date_new_start[4:8] + date_new_start[0:4]
        date.table_timeliner_col_start = date_use_start
        date_end = date.table_timeliner_col_end
        date_new_end = str(date_end).replace('-', '/')
        date_use_end = date_new_end[-2:] + date_new_end[4:8] + date_new_end[0:4]
        date.table_timeliner_col_end = date_use_end
    return render(request, 'manager/manager.html',
                  {'evalname': evalname, 'timeevalname': timeevalname, 'user_name': administrator,
                   'timeline_list': timeline_list, 'dateline': dateline, 'admin': administrator})


def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/')
    request.session.flush()
    return redirect('/')


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'login/password_reset_form.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            try:
                user_email = models.TableUser.objects.get(table_user_col_email=email)
            except:
                message = "您的邮箱不存在，请校对后输入"
                return render(request, 'login/password_reset_form.html', locals())
            send_register_email(email, 'forget')
            return render(request, 'login/password_reset_done.html')
        else:
            message = "输入有误，请重新输入"
            return render(request, 'login/password_reset_form.html', locals())


class ResetView(View):
    def get(self, request, active_code):
        record = models.TableUser.objects.filter(table_user_col_code=active_code)
        print(record)
        if record:
            for i in record:
                email = i.email
                is_register = models.TableUser.objects.filter(table_user_col_email=email)
                if is_register:
                    return render(request, 'login/password_reset_confirm.html', {'email': email})
        return redirect('/')


class ModifyView(View):
    def post(self, request):
        reset_form = ResetForm(request.POST)
        if reset_form.is_valid():
            pwd1 = request.POST.get('newpwd1', '')
            pwd2 = request.POST.get('newpwd2', '')
            email = request.POST.get('email', '')
            if pwd1 != pwd2:
                return render(request, 'login/password_reset_confirm.html', {'msg': '密码不一致！'})
            else:
                user = models.TableUser.objects.get(table_user_col_email=email)
                user.table_user_col_password = make_password(pwd2)
                user.save()
                return redirect('/modifydone')
        else:
            email = request.POST.get('email', '')
            return render(request, 'login/password_reset_confirm.html', {'msg': reset_form.errors})


def Modifydone(request):
    return render(request, 'login/modifydone.html')


def abstract(request):
    return render(request, 'login/abstract.html')


def Aboutus(request):
    return render(request, 'login/Aboutus.html')


def download_form(request):
    question_id = request.GET.get('form')
    user_name = request.session['user_name']
    user_info = TableUser.objects.get(table_user_col_name=user_name)
    user_real_name = user_info.table_user_col_real_name
    user_org = user_info.table_user_col_organization_id
    print(user_org)
    user_org_name = TableOrganization.objects.get(table_organization_col_id=user_org).table_organization_col_name
    select_question = TableQuestionContent.objects.get(table_question_content_col_question_id=question_id)
    indicator_id = select_question.table_question_content_col_indicator_id
    question_num = select_question.table_question_content_col_question_number
    # content转化为字典
    question_content = eval(select_question.table_question_content_col_content)
    content_title = question_content['title']
    content_column = question_content['column']

    workbook = Workbook(encoding='utf-8')
    file_name = u"form_" + str(indicator_id) + "_" + str(question_num) + ".xls"
    sheet_str = "" + str(question_id) + "_" + str(indicator_id) + "_" + str(question_num)
    worksheet = workbook.add_sheet(sheet_str)

    # 样式
    style = xlwt.XFStyle()  # 创建一个样式对象，初始化样式
    al = xlwt.Alignment()
    al.horz = 0x02  # 设置水平居中
    al.vert = 0x01  # 设置垂直居中
    style.alignment = al
    style.alignment.wrap = 1
    # 设置行高
    tall_style = xlwt.easyxf('font:height 720;')  # 36pt,类型小初的字号
    for num in range(0, 20):
        row_set = worksheet.row(num)
        row_set.set_style(tall_style)
    # 设置列宽
    for num in range(0, 10):
        worksheet.col(num).width = 150 * 20

    worksheet.write(0, 0, "题目", style)
    worksheet.write(0, 1, "id", style)
    worksheet.write(0, 2, "指标id", style)
    worksheet.write(0, 3, "题号", style)
    worksheet.write(0, 4, "用户", style)
    worksheet.write(0, 5, "姓名", style)
    worksheet.write(0, 6, "单位", style)

    worksheet.write(1, 0, content_title, style)
    worksheet.write(1, 1, question_id, style)
    worksheet.write(1, 2, indicator_id, style)
    worksheet.write(1, 3, question_num, style)
    worksheet.write(1, 4, user_name, style)
    worksheet.write(1, 5, user_real_name, style)
    worksheet.write(1, 6, user_org_name, style)

    for x in range(0, len(content_column)):
        worksheet.write(2, x, str(x + 1), style)
        worksheet.write(3, x, content_column[x], style)

    output = BytesIO()
    workbook.save(output)
    output.seek(0)
    response = HttpResponse(output.getvalue(), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(escape_uri_path(file_name))
    response.write(output.getvalue())
    return response
    # question_id = request.GET.get('form')
    # select_question = TableQuestionContent.objects.get(table_question_content_col_question_id=question_id)
    # indicator_id = select_question.table_question_content_col_indicator_id
    # question_num = select_question.table_question_content_col_question_number
    # # content转化为字典
    # question_content = eval(select_question.table_question_content_col_content)
    # content_title = question_content['title']
    # content_column = question_content['column']
    #
    # workbook = Workbook(encoding='utf-8')
    # file_name = u"form_" + str(indicator_id) + "_" + str(question_num) + ".xls"
    # sheet_str = "" + str(question_id) + "_" + str(indicator_id) + "_" + str(question_num)
    # worksheet = workbook.add_sheet(sheet_str)
    #
    # # 样式
    # style = xlwt.XFStyle()  # 创建一个样式对象，初始化样式
    # al = xlwt.Alignment()
    # al.horz = 0x02  # 设置水平居中
    # al.vert = 0x01  # 设置垂直居中
    # style.alignment = al
    # style.alignment.wrap = 1
    # # 设置行高
    # tall_style = xlwt.easyxf('font:height 720;')  # 36pt,类型小初的字号
    # for num in range(0, 20):
    #     row_set = worksheet.row(num)
    #     row_set.set_style(tall_style)
    # # 设置列宽
    # for num in range(0, 10):
    #     worksheet.col(num).width = 150 * 20
    #
    # worksheet.write(0, 0, "题目", style)
    # worksheet.write(0, 1, "id", style)
    # worksheet.write(0, 2, "指标id", style)
    # worksheet.write(0, 3, "题号", style)
    #
    # worksheet.write(1, 0, content_title, style)
    # worksheet.write(1, 1, question_id, style)
    # worksheet.write(1, 2, indicator_id, style)
    # worksheet.write(1, 3, question_num, style)
    #
    # for x in range(0, len(content_column)):
    #     worksheet.write(2, x, str(x + 1), style)
    #     worksheet.write(3, x, content_column[x], style)
    #
    # output = BytesIO()
    # workbook.save(output)
    # output.seek(0)
    # response = HttpResponse(output.getvalue(), content_type='application/vnd.ms-excel')
    # response['Content-Disposition'] = 'attachment;filename="{0}"'.format(escape_uri_path(file_name))
    # response.write(output.getvalue())
    # return response

def upload_xlsx(request):
    """ 导入Excel数据 """
    if request.method == 'POST':
        try:
            with transaction.atomic():  # 事物
                excel = request.FILES.get('file_obj')
                book = xlrd.open_workbook(filename=None, file_contents=excel.read())
                sheet = book.sheet_by_index(0)
                num_row = sheet.nrows

                if num_row == 4:
                    return HttpResponse('未填写数据')

                user_info = sheet.row_values(1)
                question_title = user_info[0]  # 题目内容
                question_id = user_info[1]  # 题目id
                question_indicator_id = user_info[2]  # 题目对应指标id
                question_num = user_info[3]  # 题目id
                question_user = user_info[4]  # 填写题目的用户
                question_user_realname = user_info[5]  # 用户真实姓名
                question_user_org = user_info[6]  # 用户单位id

                line_2 = sheet.row_values(2)
                line_length = len(line_2)
                flag = 0
                for x in range(0, line_length):
                    if len(line_2[x]) == 0:
                        flag = x
                        break
                if flag != 0:
                    line_length = flag

                list_form = []
                for row in range(4, num_row):
                    line = sheet.row_values(row)
                    tmp = []
                    if line_length < 7:
                        for x in range(0, line_length):
                            tmp.append(line[x])
                        list_form.append(tmp)
                    else:
                        list_form.append(line)

                store_answer = {'title': question_title, 'answer': list_form}
                store_mark = TableQuestionContent.objects.get(
                    table_question_content_col_question_id=question_id).table_question_content_col_marks
                if len(store_mark) == 0:
                    store_mark = 0
                store_user_id = TableUser.objects.get(
                    Q(table_user_col_name=question_user) & Q(table_user_col_real_name=question_user_realname)).table_user_col_id
                store_questionaire_id = 1
                store_question_id = TableQuestionContent.objects.get(
                    table_question_content_col_question_id=question_id).table_question_content_col_question_id

                if TableQuestionResult.objects.filter(Q(table_question_result_col_user_id=store_user_id) & Q(table_question_result_col_question_id=store_question_id)).exists():
                    TableQuestionResult.objects.filter(Q(table_question_result_col_user_id=store_user_id) & Q(
                        table_question_result_col_question_id=store_question_id)).update(
                        table_question_result_col_answer=store_answer,
                        table_question_result_col_marks=store_mark,
                    )
                else:
                    store_blank = ''.join(random.sample(string.ascii_letters + string.digits, 20))  # 创建blank随机名
                    new_record = {
                        "table_question_result_col_answer": store_answer,
                        "table_question_result_col_marks": store_mark,
                        "table_question_result_col_blank": store_blank,
                        "table_question_result_col_user_id": store_user_id,
                        "table_question_result_col_questionaire_id": store_questionaire_id,
                        "table_question_result_col_question_id": store_question_id,
                    }
                    # print(new_record)
                    TableQuestionResult.objects.create(**new_record)

                return HttpResponse('OK')
        except Exception as e:
            print(e)
            # return render(request, 'user/user.html')
            return HttpResponse('error')
    pass
    # return render(request, 'user/user.html')

