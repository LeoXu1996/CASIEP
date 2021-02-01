# from . import forms
import random
import string
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password

from django.shortcuts import redirect
from django.shortcuts import render
from django.views import View

from administrator.models import TableTimeliner, TableQuestionContent
from login import models
from login.forms import ForgetForm, ResetForm
from login.utils.email_send import send_register_email

from supervisor.models import TableEvaluation

from supervisor.models import TableOrganization
from administrator.models import TableTimeliner,TableQuestionResult
from login import models
import datetime
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
import xlwt
from io import BytesIO
from xlwt import Workbook
from django.utils.encoding import escape_uri_path


def user(request):
    user_name = request.session['user_name']
    current_eval = request.GET.get('evalname')
    # print(current_eval)
    orgid = \
        models.TableUser.objects.filter(table_user_col_name=user_name).values_list('table_user_col_organization')[0][0]
    orgname = \
    TableOrganization.objects.filter(table_organization_col_id=orgid).values_list('table_organization_col_name')[0][
            0]
    eval = TableEvaluation.objects.filter(table_evaluation_col_name=current_eval)
    if len(eval) != 0:
        questionaire_answer = set(
            TableQuestionContent.objects.filter(
                table_question_content_col_evalname=eval[0].table_evaluation_col_id).values_list(
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
            # print(question)
            return render(request, 'user/user.html',
                          { 'current_eval':current_eval,'question': question,
                           'preview_length': len(list),
                           'user': user_name, 'orgname': orgname, 'page_num': page_num})
        else:
            return render(request, 'user/user.html', {'current_eval':current_eval,'user': user_name, 'orgname': orgname})
    else:
        return render(request, 'user/user.html', {'current_eval':current_eval,'user': user_name, 'orgname': orgname})


def questionaire_submit(request):
    print(request.POST)
    return JsonResponse({'msg': 'success'})


def answer_save(request):
    user_name = request.session['user_name']
    print(user_name)
    if request.method == 'POST':
        question_class = request.POST['questionclass']
        question_type = request.POST['questiontype']

        print(question_type)
        if question_type == "填空题":
            store_answer = request.POST['send_info']
            store_answer = store_answer.replace('[', '')
            store_answer = store_answer.replace(']', '')
            store_answer = store_answer.replace('\"', '')
            store_answer = store_answer.split(",")
            for i in range(0, len(store_answer)):
                if len(store_answer[i]) == 0:
                    return JsonResponse({'message': 'Done'})
        elif question_type == "选择题" or "简答题" or "矩阵题":
            if question_class == "单选":
                store_answer = request.POST['send_info']
            else:
                store_answer = request.POST['send_info']
                store_answer = store_answer.replace('[', '')
                store_answer = store_answer.replace(']', '')
                store_answer = store_answer.replace('\"', '')
                store_answer = store_answer.split(",")

        store_question_id = request.POST['questionid']
        store_mark = 0
        tmp = TableQuestionContent.objects.get(table_question_content_col_question_id=store_question_id).table_question_content_col_marks
        if len(tmp) != 0:
            store_mark = tmp
        store_user_id = models.TableUser.objects.get(table_user_col_name=user_name).table_user_col_id
        store_questionaire_id = 0

        if TableQuestionResult.objects.filter(
            table_question_result_col_user_id=store_user_id).exists() & TableQuestionResult.objects.filter(
            table_question_result_col_question_id=store_question_id).exists():
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
            print(new_record)
            TableQuestionResult.objects.create(**new_record)

    return JsonResponse({'message': 'Done'})
# def visualization(request):
#     check_app = request.GET.get('app')
#     return render(request, 'visual/overview_research.html', {'check_app': check_app})