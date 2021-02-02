from __future__ import unicode_literals

import ast
import codecs
import csv
import datetime
import io
import json
import os
import random
import shutil
import string
import tempfile
import time
import zipfile
from decimal import *
from io import BytesIO

import xlrd
import xlwt
from django.core import serializers
from django.db.models import Q
from django.http import JsonResponse, FileResponse
from django.shortcuts import HttpResponse, render
from django.utils.encoding import escape_uri_path
from django.utils.http import urlquote
from xlwt import Workbook

from DESP import settings
from administrator import models
from administrator.models import TableEvaluationIndicator, TableQuestionContent, TableUploadFile
from login.models import TableUser
from supervisor.models import TableEvaluation
from supervisor.models import TableOrganization


def test(request):
    if request.method == "POST":
        manager = request.session.get('user_name')
        pro_name_eval = request.POST.get("pro_name_d_1")
        pro_name = request.POST.get("pro_name_d_2")
        print("----")
        print(manager)
        print(pro_name_eval)
        print(pro_name)
        print("----")

    # if request.method == "POST":    # 请求方法为POST时，进行处理
    #     form = request.POST.get("form_auto")
    #     pro_name_eval = request.POST.get("pro_name_d_1")
    #     pro_name = request.POST.get("pro_name_d_2")
    #
    #     print("----")
    #     print(form)
    #     print(pro_name_eval)
    #     print(pro_name)
    #     print("----")

    return JsonResponse({'message': 'Done'})


def download_file(request):
    if request.method == "POST":
        pro_name_eval = request.POST.get("pro_name_d_1")
        pro_name = request.POST.get("pro_name_d_2")
        tmp = "length_" + pro_name
        file_num = request.POST.get(tmp)
        tmp = "checkall_" + pro_name
        check_all = request.POST.get(tmp)

        file_name = []
        if check_all == "select":
            for x in range(0, int(file_num)):
                text = "checkson" + str(x)
                tmp = request.POST.get(text)
                file_name.append(tmp)
        else:
            for x in range(0, int(file_num)):
                text = "checksoncheck" + pro_name + str(x)
                tmp = request.POST.get(text)
                if tmp == "select":
                    text = "checkson" + str(x)
                    tmp = request.POST.get(text)
                    file_name.append(tmp)

        co_dict = []
        filenames = []
        for x in file_name:
            file_record = TableUploadFile.objects.get(table_upload_file_col_name=x)
            tmp = {}
            tmp['download_url'] = 'uploadFile/' + file_record.table_upload_file_col_cover
            tmp['name'] = file_record.table_upload_file_col_name
            co_dict.append(tmp)
            filenames.append('uploadFile/' + file_record.table_upload_file_col_cover)

        if len(co_dict) == 1:
            for x in co_dict:
                filename = x['name']
                filepath = x['download_url']
                file = open(filepath, 'rb')
                response = FileResponse(file)
                response['Content-Type'] = 'application/octet-stream'
                response['Content-Disposition'] = 'attachment;filename="{0}"'.format(escape_uri_path(filename))
                return response
        else:
            zip_sub = "Proj_" + str(pro_name)
            zip_name = zip_sub + ".zip"
            s = io.BytesIO()
            zf = zipfile.ZipFile(s, "w")
            for f in co_dict:
                f_url = 'uploadFile/' + f['name']
                print(f_url)
                shutil.copy(f['download_url'], f_url)
                fdir, fname = os.path.split(f_url)
                zip_path = os.path.join(zip_sub, fname)
                zf.write(f_url, zip_path)
                os.remove(f_url)
            zf.close()
            response = HttpResponse(s.getvalue(), content_type="application/x-zip-compressed")
            response['Content-Disposition'] = 'attachment; filename="{0}"'.format(escape_uri_path(zip_name))
            return response


def upload_file(request):
    if request.method == "POST":  # 请求方法为POST时，进行处理
        myFile = request.FILES.get("myfile", None)  # 获取上传的文件，如果没有文件，则默认为None
        if not myFile:
            # return HttpResponse({'message': 'no files for upload!'})
            return render(request, 'standard/timeliner.html')
            # return render(request, 'standard/timeliner.html', {'upload_flag': True})

        pro_name_eval = request.POST.get("pro_name_1")
        pro_name = request.POST.get("pro_name_2")
        now = datetime.datetime.now()  # 获得当前时间
        random_name = ''.join(random.sample(string.ascii_letters + string.digits, 20))  # 创建随机名

        if TableUploadFile.objects.filter(Q(table_upload_file_col_name=myFile.name)).exists():
            record = TableUploadFile.objects.get(table_upload_file_col_name=myFile.name)
            if record.table_upload_file_col_evaluation == pro_name_eval:
                if record.table_upload_file_col_timeliner == pro_name:
                    # 删除已有文件
                    delete_file_path = settings.BASE_DIR + os.sep + "uploadFile" + os.sep + record.table_upload_file_col_cover
                    if os.path.exists(delete_file_path):
                        os.remove(delete_file_path)
                    # 修改数据库记录
                    record.table_upload_file_col_time = now
                    record.table_upload_file_col_cover = random_name
                    record.save()
        else:
            new_record = {
                "table_upload_file_col_name": myFile.name,
                "table_upload_file_col_time": now,
                "table_upload_file_col_evaluation": pro_name_eval,
                "table_upload_file_col_timeliner": pro_name,
                "table_upload_file_col_cover": random_name
            }
            models.TableUploadFile.objects.create(**new_record)

        destination = open(os.path.join("uploadFile", random_name), 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()

        return JsonResponse({'message': 'Done'})


def export_questionaire(request):
    q_e = request.GET.get('questionaire_evalname')
    file_name = u"questionaire_" + str(q_e) + ".xls"
    workbook = Workbook(encoding='utf-8')
    id=''
    # 查询项目对应的机构名称id作为parentid
    select_org = models.TableEvaluation.objects.get(Q(table_evaluation_col_name=q_e)).table_evaluation_col_organization
    # print(select_org)
    for each in select_org:
        if each != ',':
            id+=each
        else:
            # print(id)
            # parent_org_id = TableOrganization.objects.get(Q(table_organization_col_id=int(id))).table_organization_col_id
            break

    list_indicator = models.TableEvaluationIndicator.objects.filter(
        Q(table_evaluation_indicator_col_evaluation_name=q_e) &
        Q(table_evaluation_indicator_col_parent_name_id__isnull=False)). \
        order_by('table_evaluation_indicator_col_id')

    for x1 in list_indicator:
        list_questionaire = models.TableQuestionContent.objects.filter(
            Q(table_question_content_col_question_importanswer='on') &
            Q(table_question_content_col_indicator_id=x1.table_evaluation_indicator_col_id)). \
            order_by('table_question_content_col_question_number')
        for x2 in list_questionaire:
            TQC_indicator_id = str(x2.table_question_content_col_indicator_id)
            TQC_question_number = str(x2.table_question_content_col_question_number)
            TQC_markmethod = str(x2.table_question_content_col_markmethod)
            TQC_question_attachment = str(x2.table_question_content_col_question_attachment)
            TQC_question_class = str(x2.table_question_content_col_question_class)
            TQC_question_importanswer = str(x2.table_question_content_col_question_importanswer)
            TQC_question_required = str(x2.table_question_content_col_question_required)
            TQC_question_type = str(x2.table_question_content_col_question_type)
            TQC_content_dict = ast.literal_eval(x2.table_question_content_col_content)  # 转换成字典
            TQC_content_title = str(TQC_content_dict['title'])

            sheet_str = "" + str(TQC_indicator_id) + "-" + str(TQC_question_number)
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

            # 写入 sheet
            worksheet.write(0, 0, "指标id", style)
            worksheet.write(0, 1, "问题编号", style)
            worksheet.write(0, 2, "计分方式", style)
            worksheet.write(0, 3, "question_attachment", style)
            worksheet.write(0, 4, "question_importanswer", style)
            worksheet.write(0, 5, "question_required", style)
            worksheet.write(0, 6, "问题种类", style)
            worksheet.write(0, 7, "问题类型", style)
            worksheet.write(2, 0, "题目", style)
            worksheet.write(4, 0, "机构名称", style)
            worksheet.write(4, 1, "机构id", style)
            # 填入数据
            worksheet.write(1, 0, TQC_indicator_id, style)
            worksheet.write(1, 1, TQC_question_number, style)
            worksheet.write(1, 2, TQC_markmethod, style)
            worksheet.write(1, 3, TQC_question_attachment, style)
            worksheet.write(1, 4, TQC_question_importanswer, style)
            worksheet.write(1, 5, TQC_question_required, style)
            worksheet.write(1, 6, TQC_question_type, style)
            worksheet.write(1, 7, TQC_question_class, style)
            worksheet.write_merge(2, 2, 1, 7, TQC_content_title, style)  # 合并单元格用于填写题目

            if TQC_question_type == "填空题":
                tmp = '_'.join(filter(lambda x: x, TQC_content_title.split('_')))
                count = tmp.count('_')
                worksheet.write(3, 0, "填空数", style)
                worksheet.write(3, 1, str(count), style)
                for x in range(0, count):
                    worksheet.write(3, x + 2, "填空" + str(x + 1), style)

            if TQC_question_type == "选择题":
                TQC_content_answer = TQC_content_dict['answer']
                count = len(TQC_content_answer)
                worksheet.write(3, 0, "选择数", style)
                worksheet.write(3, 1, str(count), style)
                worksheet.write(3, 2 + count, "选项填'1'", style)
                for x in range(0, count):
                    worksheet.write(3, x + 2, TQC_content_answer[x], style)

            # if TableOrganization.objects.filter(Q(table_organization_col_parent_name_id=parent_org_id)).exists():
            #     org_id = TableOrganization.objects.filter(Q(table_organization_col_parent_name_id=parent_org_id))
            #     count = 0
            #     for n in org_id:
            #         TO_org_name = str(n.table_organization_col_name)
            #         TO_org_id = str(n.table_organization_col_id)
            #         worksheet.write(5 + count, 0, TO_org_name, style)
            #         worksheet.write(5 + count, 1, TO_org_id, style)
            #         count = count + 1
            # else:
            id=''
            for each in select_org:
                if each != ',':
                    id += each
                else:
                    # org_id = parent_org_id
                    # print(id)
                    TO_org_name =TableOrganization.objects.get(Q(table_organization_col_id=int(id))).table_organization_col_name
                    TO_org_id = str(id)
                    worksheet.write(5 + count, 0, TO_org_name, style)
                    worksheet.write(5 + count, 1, TO_org_id, style)
                    count+=1
                    id=''

    output = BytesIO()
    workbook.save(output)
    output.seek(0)
    response = HttpResponse(output.getvalue(), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(escape_uri_path(file_name))
    response.write(output.getvalue())
    return response



def standard(request):
    mList = TableEvaluationIndicator.objects.filter(
        Q(table_evaluation_indicator_col_evaluation_name=request.GET.get('evalname')) &
        Q(table_evaluation_indicator_col_administrator_name=request.session.get('user_name')))
    current_eval = request.GET.get('evalname')
    current_admin = request.session.get('user_name')
    if mList.exists():
        _data = [
            {
                'id': x.table_evaluation_indicator_col_id,
                'name': x.table_evaluation_indicator_col_name + '   (' + str(
                    x.table_evaluation_indicator_col_weight) + '%)',
                'pId': x.table_evaluation_indicator_col_parent_name.table_evaluation_indicator_col_id if x.table_evaluation_indicator_col_parent_name else 0,
                'open': 1,
            } for x in mList
        ]

        evalobj = TableEvaluation.objects.get(table_evaluation_col_name=current_eval)
        questionaire_preview = set(
            TableQuestionContent.objects.filter(table_question_content_col_evalname=evalobj).values_list(
                'table_question_content_col_indicator_id'))
        group = []
        for eachquestion in questionaire_preview:
            group.append(eachquestion)
        id = request.GET.get('id')
        indiname = current_eval
        notroot = 0
        for each in _data:
            if each['id'] == int(id):
                indiname = each['name']
            if each['pId'] == int(id):
                notroot += 1;
        index = 0
        for each in group:
            if each[0] == int(id):
                break
            else:
                index = index + 1
        list = []
        for i in range(0, len(questionaire_preview)):
            list.append(TableQuestionContent.objects.filter(table_question_content_col_indicator_id=group[i][0]))

        preview = []
        if index == None:
            for x in list[0]:
                print(x)
                preview.append({
                    'question_type': x.table_question_content_col_question_type,
                    'content': x.table_question_content_col_content
                })
        elif index >= len(list):
            print("no question here")
        else:
            for x in list[index]:
                preview.append({
                    'question_type': x.table_question_content_col_question_type,
                    'content': x.table_question_content_col_content
                })
        administrator = request.session['user_name']
        evalname = TableEvaluation.objects.filter(
            Q(table_evaluation_col_administrator=administrator) & Q(table_evaluation_col_status='启用')).values(
            'table_evaluation_col_name')
        timeevalname = models.TableTimeliner.objects.values('table_timeliner_col_evaluation').distinct().order_by(
            'table_timeliner_col_evaluation')
        return render(request, 'standard/standard.html',
                      {'question': preview, 'data': _data, 'evalname': evalname, 'admin': administrator,
                       'timeevalname': timeevalname, 'id': id, 'notroot': notroot, 'indiname': indiname,
                       'current_eval': current_eval, 'current_admin': current_admin, 'preview_length': len(list),
                       'questionlist': list})

    else:
        administrator = request.session['user_name']
        evallist = TableEvaluation.objects.filter(
            Q(table_evaluation_col_administrator=administrator) & Q(
                table_evaluation_col_status='启用') & Q(table_evaluation_col_name=request.GET.get('evalname')))
        if evallist.exists():
            root = {
                "table_evaluation_indicator_col_name": request.GET.get('evalname'),
                "table_evaluation_indicator_col_parent_name": None,
                "table_evaluation_indicator_col_weight": 100.00,
                "table_evaluation_indicator_col_evaluation_name": request.GET.get('evalname'),
                "table_evaluation_indicator_col_administrator_id": request.session['user_id'],
                "table_evaluation_indicator_col_administrator_name": administrator
            }
            TableEvaluationIndicator.objects.create(**root)
            rList = TableEvaluationIndicator.objects.filter(
                table_evaluation_indicator_col_evaluation_name=request.GET.get('evalname'),
                table_evaluation_indicator_col_administrator_name=request.session.get('user_name'))
            _data = [
                {
                    'id': x.table_evaluation_indicator_col_id,
                    'name': x.table_evaluation_indicator_col_name + '   (' + str(
                        x.table_evaluation_indicator_col_weight) + '%)',
                    'pId': x.table_evaluation_indicator_col_parent_name.table_evaluation_indicator_col_id if x.table_evaluation_indicator_col_parent_name else 0,
                    'open': 1,
                } for x in rList
            ]
            evalname = TableEvaluation.objects.filter(
                Q(table_evaluation_col_administrator=administrator) & Q(table_evaluation_col_status='启用')).values(
                'table_evaluation_col_name')
            timeevalname = models.TableTimeliner.objects.values('table_timeliner_col_evaluation').distinct().order_by(
                'table_timeliner_col_evaluation')
            return render(request, 'standard/standard.html',
                          {'data': _data, 'evalname': evalname, 'admin': administrator, 'timeevalname': timeevalname,
                           'current_eval': current_eval})
        else:
            return JsonResponse({'message': '您输入的用户或评估项目不存在'})  # 增加返回到administrator页面 及message显示的功能


def delete(request):
    if request.method == 'POST':
        delete_id = request.POST.get('delete_id')

        try:
            TableEvaluationIndicator.objects.filter(
                table_evaluation_indicator_col_id=delete_id).delete()

            return JsonResponse({'state': 1, 'message': '删除成功!'})
        except Exception as e:
            return JsonResponse({'state': 0, 'message': 'Create Error: ' + str(e)})


def edit(request):
    administrator = request.session['user_name']
    if request.method == 'GET':
        edit_id = request.GET.get('edit_id')
        List = TableEvaluationIndicator.objects.filter(
            Q(table_evaluation_indicator_col_id=edit_id) |
            Q(table_evaluation_indicator_col_parent_name=edit_id))
        mList = serializers.serialize('json', List)
        return JsonResponse({'data': mList})
    if request.method == 'POST':
        # pdb.set_trace()
        editdata = eval(request.POST.get('datalist'))
        del editdata[0]
        print(editdata)
        create_parent = editdata[0][0]
        print(create_parent)
        evalname = TableEvaluationIndicator.objects.filter(table_evaluation_indicator_col_id=create_parent).values_list(
            'table_evaluation_indicator_col_evaluation_name')[0][0]
        print(evalname)
        for item in editdata:
            if item[0] == "":
                postdata = {
                    "table_evaluation_indicator_col_name": item[1],
                    "table_evaluation_indicator_col_parent_name": TableEvaluationIndicator.objects.get(
                        table_evaluation_indicator_col_id=create_parent),
                    "table_evaluation_indicator_col_weight": item[2],
                    "table_evaluation_indicator_col_evaluation_name": evalname,
                    "table_evaluation_indicator_col_administrator_id": request.session['user_id'],
                    "table_evaluation_indicator_col_administrator_name": administrator
                }
                list = []
                for a in TableEvaluationIndicator.objects.filter(
                        Q(table_evaluation_indicator_col_parent_name=create_parent)):
                    list.append(a.table_evaluation_indicator_col_weight)
                result = sum(list)
                if result + round(Decimal(float(item[2])), 2) <= 100:
                    try:
                        TableEvaluationIndicator.objects.create(**postdata)
                        continue
                    except Exception as e:
                        return JsonResponse({'message': 'Edit Error: ' + str(e)})
                else:
                    return JsonResponse({'message': '子级指标的和不应超过100%哦'})
            else:
                print('root')
                postdata_edit = {
                    "table_evaluation_indicator_col_name": item[1],
                    "table_evaluation_indicator_col_weight": item[2],
                }
                print(postdata_edit)
                list = []
                parentid = \
                    TableEvaluationIndicator.objects.filter(table_evaluation_indicator_col_id=item[0]).values_list(
                        'table_evaluation_indicator_col_parent_name')[0][0]
                # if parentid==None:
                #     break
                print(parentid)
                # for a in TableEvaluationIndicator.objects.filter(
                #         Q(table_evaluation_indicator_col_parent_name=parentid) &
                #         ~Q(
                #             table_evaluation_indicator_col_id=item[0])):
                #     print(a)
                #     list.append(a.table_evaluation_indicator_col_weight)
                #     print(list)
                result = 0
                for each in editdata:
                    list.append(float(each[2]))
                    # print(each[2])
                result = sum(list[1:])
                print(result)
                if parentid != None:
                    if result <= 100:
                        try:
                            TableEvaluationIndicator.objects.filter(
                                table_evaluation_indicator_col_id=item[0]).update(**postdata_edit)
                            continue
                        except Exception as e:
                            return JsonResponse({'message': 'Edit Error: ' + str(e)})
                    else:
                        return JsonResponse({'message': '子级指标的和不应超100%'})
        return JsonResponse({'message': '修改成功!'})


def indicator_export(request):
    # pdb.set_trace()
    response = HttpResponse(content_type='text/csv')
    response.write(codecs.BOM_UTF8)
    response['Content-Disposition'] = "attachment;filename=evaluation_indicator.csv"
    writer = csv.writer(response)
    page_eval = request.GET.get('current_eval')
    indicator = models.TableEvaluationIndicator.objects.filter(table_evaluation_indicator_col_evaluation_name=page_eval)
    writer.writerow(['Indicator_Name', 'Indicator_Weight', 'Indicator_Parent_Name'])
    write_length = len(indicator)
    write_position = 1
    while write_position < write_length:
        # pdb.set_trace()
        try:
            indicator_row = indicator[write_position]
            select_parent = models.TableEvaluationIndicator.objects.get(table_evaluation_indicator_col_name=page_eval)
        except:
            return JsonResponse({'message': '没有数据可导出'})
        if indicator_row.table_evaluation_indicator_col_parent_name == select_parent:
            try:
                writer.writerow([indicator_row.table_evaluation_indicator_col_name,
                                 indicator_row.table_evaluation_indicator_col_weight])
                write_position += 1
            except:
                return JsonResponse({'message': '高级节点数据缺失'})
        else:
            try:
                parent_key = indicator_row.table_evaluation_indicator_col_parent_name
                writer.writerow([indicator_row.table_evaluation_indicator_col_name,
                                 indicator_row.table_evaluation_indicator_col_weight,
                                 parent_key.table_evaluation_indicator_col_name])
                write_position += 1
            except:
                return JsonResponse({'message': '节点数据缺失'})

    return response


def timeliner(request):
    # pdb.set_trace()
    administrator = request.session['user_name']
    current_eval = request.GET.get('timeevalname')
    evalname = TableEvaluation.objects.filter(
        Q(table_evaluation_col_administrator=administrator) & Q(table_evaluation_col_status='启用')).values(
        'table_evaluation_col_name')
    timeevalname = models.TableTimeliner.objects.values('table_timeliner_col_evaluation').distinct().order_by(
        'table_timeliner_col_evaluation')
    timeline_list = models.TableTimeliner.objects.filter(
        table_timeliner_col_evaluation=request.GET.get('timeevalname')).order_by('table_timeliner_col_start')
    dateline_list = models.TableTimeliner.objects.filter(
        table_timeliner_col_evaluation=request.GET.get('timeevalname')).order_by('table_timeliner_col_start')

    test_list = []
    if TableUploadFile.objects.filter(Q(table_upload_file_col_evaluation=current_eval)):
        # test_list_tmp_0 = TableUploadFile.objects.get(table_upload_file_col_evaluation=current_eval)
        for x in timeline_list:
            tmp = []
            if TableUploadFile.objects.filter(Q(table_upload_file_col_evaluation=current_eval)
                                              & Q(table_upload_file_col_timeliner=x.table_timeliner_col_name)):
                test_list_tmp_1 = TableUploadFile.objects.filter(Q(table_upload_file_col_evaluation=current_eval)
                                                                 & Q(
                    table_upload_file_col_timeliner=x.table_timeliner_col_name))
                for y in test_list_tmp_1:
                    tmp.append({
                        'file_name': y.table_upload_file_col_name,
                    })
            test_list.append({
                'table_timeliner_col_id': x.table_timeliner_col_id,
                'table_timeliner_col_start': x.table_timeliner_col_start,
                'table_timeliner_col_name': x.table_timeliner_col_name,
                'table_timeliner_col_content': x.table_timeliner_col_content,
                'table_timeliner_col_end': x.table_timeliner_col_end,
                'table_timeliner_col_status': x.table_timeliner_col_status,
                'table_upload_file': tmp,
            })
    else:
        for x in timeline_list:
            tmp = []
            test_list.append({
                'table_timeliner_col_id': x.table_timeliner_col_id,
                'table_timeliner_col_start': x.table_timeliner_col_start,
                'table_timeliner_col_name': x.table_timeliner_col_name,
                'table_timeliner_col_content': x.table_timeliner_col_content,
                'table_timeliner_col_end': x.table_timeliner_col_end,
                'table_timeliner_col_status': x.table_timeliner_col_status,
                'table_upload_file': tmp,
            })

    date_length = len(dateline_list)
    order_list = []
    order_count = 0
    while order_count < date_length:
        order_list.append(dateline_list.values_list('table_timeliner_col_id')[order_count][0])
        order_count = order_count + 1
    dateline = models.TableTimeliner.objects.filter(pk__in=order_list)
    for date in dateline:
        date_start = date.table_timeliner_col_start
        date_new_start = str(date_start).replace('-', '/')
        date_use_start = date_new_start[-2:] + date_new_start[4:8] + date_new_start[0:4]
        date.table_timeliner_col_start = date_use_start
        date_end = date.table_timeliner_col_end
        date_new_end = str(date_end).replace('-', '/')
        date_use_end = date_new_end[-2:] + date_new_end[4:8] + date_new_end[0:4]
        date.table_timeliner_col_end = date_use_end
    return render(request, 'standard/timeliner.html',
                  {'evalname': evalname, 'admin': administrator, 'timeevalname': timeevalname,
                   'test_list': test_list,
                   'timeline_list': timeline_list, 'dateline': dateline, 'current_eval': current_eval})


def timeliner_create(request):
    if request.method == 'POST':
        # pdb.set_trace()
        timeliner_name = request.POST.get('name')
        timeliner_content = request.POST.get('content')
        timeliner_status = request.POST.get('status')
        timeliner_start = request.POST.get('start')
        timeliner_end = request.POST.get('end')
        timeliner_eval = request.POST.get('eval')
        if timeliner_end > timeliner_start:
            try:
                models.TableTimeliner.objects.create(table_timeliner_col_name=timeliner_name,
                                                     table_timeliner_col_content=timeliner_content,
                                                     table_timeliner_col_status=timeliner_status,
                                                     table_timeliner_col_start=timeliner_start,
                                                     table_timeliner_col_end=timeliner_end,
                                                     table_timeliner_col_evaluation=timeliner_eval
                                                     )
                return JsonResponse({'state': 1, 'message': '创建成功!'})
            except Exception as e:
                return JsonResponse({'state': 0, 'message': 'Create Error: ' + str(e)})
        else:
            return JsonResponse({'message': '结束时间不得晚于开始时间！'})


def timeliner_edit(request):
    if request.method == 'GET':
        timeliner_id = request.GET.get('edit_id')
        timeline = serializers.serialize("json",
                                         models.TableTimeliner.objects.filter(table_timeliner_col_id=timeliner_id))
        # print(eva)
        return JsonResponse({'timeline': timeline})
    elif request.method == 'POST':
        # pdb.set_trace()
        timeliner_id = request.POST.get('edit_id')
        timeliner_name = request.POST.get('edit_name')
        timeliner_content = request.POST.get('content')
        timeliner_status = request.POST.get('status')
        timeliner_start = request.POST.get('start')
        timeliner_end = request.POST.get('end')
        if timeliner_end > timeliner_start:
            try:
                models.TableTimeliner.objects.filter(table_timeliner_col_id=timeliner_id).update(
                    table_timeliner_col_name=timeliner_name,
                    table_timeliner_col_content=timeliner_content,
                    table_timeliner_col_status=timeliner_status,
                    table_timeliner_col_start=timeliner_start,
                    table_timeliner_col_end=timeliner_end)
                return JsonResponse({'state': 1, 'message': '创建成功!'})
            except Exception as e:
                return JsonResponse({'state': 0, 'message': 'Create Error: ' + str(e)})
        else:
            return JsonResponse({'message': '结束时间不得晚于开始时间！'})


def timeliner_delete(request):
    # pdb.set_trace()
    if request.method == 'POST':
        timeliner_id = request.POST.get('delete_id')
        for tl_del in models.TableTimeliner.objects.filter(table_timeliner_col_id=timeliner_id):
            if tl_del.table_timeliner_col_status == '进行中':
                return JsonResponse({'message': '项目进行中，不允许删除！'})
            elif tl_del.table_timeliner_col_status == '已完成':
                return JsonResponse({'message': '已完成项目不允许删除！'})
            else:
                try:
                    models.TableTimeliner.objects.get(table_timeliner_col_id=timeliner_id).delete()
                    return JsonResponse({'state': 1, 'message': '修改成功!'})
                except Exception as e:
                    return JsonResponse({'state': 0, 'message': 'Edit Error: ' + str(e)})


## 上传功能
def excel_import_indicator(filename, this_eval_name, this_admin_name):
    # pdb.set_trace()
    file_excel = 'C:/Users/DELL/Desktop/DESP/DESP/uploads/indicator/' + str(filename)  ##存储绝对路径（随时修改）
    by_name = u'Sheet1'
    data = xlrd.open_workbook(file_excel)  # 打开excel
    table = data.sheet_by_name(by_name)  # 表单名称
    n_rows = table.nrows  # 行数
    row_dict = {}
    for row_num in range(1, n_rows):
        row = table.row_values(row_num)  # 获得每行的字段
        # seq = [row[0], row[1], row[2], row[3]]
        seq_indicator = {'Indicator_Name': row[0], 'Indicator_Weight': row[1],
                         'Indicator_Parent_Name': row[2]}
        row_dict[row_num] = seq_indicator
    data_indicator = {
        'code': '200',
        'msg': 'success',
        'data': row_dict
    }
    indicator_write = data_indicator['data']
    max_position = len(indicator_write)

    try:
        position = 1
        while position <= max_position:
            try:

                arrs = indicator_write[position]
                indicatorname = arrs['Indicator_Parent_Name']
                parent_key = models.TableEvaluationIndicator.objects.get(
                    Q(table_evaluation_indicator_col_name=indicatorname) &
                    Q(table_evaluation_indicator_col_evaluation_name=this_eval_name))
                parent_id = models.TableEvaluationIndicator.objects.filter(
                    Q(table_evaluation_indicator_col_name=indicatorname) &
                    Q(table_evaluation_indicator_col_evaluation_name=this_eval_name)).values_list(
                    'table_evaluation_indicator_col_id')[0][0]
                admin_username = this_admin_name
                admin_id = TableUser.objects.filter(table_user_col_name=admin_username).values(
                    'table_user_col_id')[0]['table_user_col_id']
            except:
                return JsonResponse({'message': '上级指标问题'})
            try:
                current_child_name = arrs['Indicator_Name']
                child_name_set = models.TableEvaluationIndicator.objects.filter(
                    table_evaluation_indicator_col_parent_name=parent_id).values(
                    'table_evaluation_indicator_col_name')
                current_name_query = {'table_evaluation_indicator_col_name': current_child_name}
            except:
                return JsonResponse({'message': '模板不应包含最高级节点'})
            try:
                if current_name_query in child_name_set:
                    return JsonResponse({'message': '指标重复命名'})
                else:
                    try:
                        add_weight = arrs['Indicator_Weight']
                        children_set = models.TableEvaluationIndicator.objects.filter(
                            table_evaluation_indicator_col_parent_name=parent_id).values_list(
                            'table_evaluation_indicator_col_weight')
                        children_lenth = len(children_set) - 1
                        # print(children_lenth)
                    except:
                        return JsonResponse({'message': '权重问题'})
                    if children_lenth == -1:
                        current_weight = 0
                    else:
                        try:
                            child_position = 0
                            weight_list = []
                            while child_position <= children_lenth:
                                try:
                                    weight_list.append(children_set[child_position][0])
                                    child_position += 1
                                    current_weight = sum(weight_list)
                                    # print(current_weight)
                                except:
                                    return JsonResponse({'message': '权重问题'})
                        except:
                            return JsonResponse({'message': '权重问题'})
                try:
                    if round(Decimal(float(add_weight)), 2) + current_weight <= 100:
                        print(Decimal(float(add_weight)))
                        print(current_weight)
                        try:
                            models.TableEvaluationIndicator.objects.create(
                                table_evaluation_indicator_col_name=arrs['Indicator_Name'],
                                table_evaluation_indicator_col_weight=arrs['Indicator_Weight'],
                                table_evaluation_indicator_col_evaluation_name=this_eval_name,
                                table_evaluation_indicator_col_administrator_id=admin_id,
                                table_evaluation_indicator_col_administrator_name=this_admin_name,
                                table_evaluation_indicator_col_parent_name=parent_key)
                        except:
                            return JsonResponse({'message': '填写格式问题'})
                    else:
                        return JsonResponse({'message': '权重问题'})
                    position = position + 1
                except:
                    return JsonResponse({'message': '权重问题'})
            except:
                return JsonResponse({'message': '检查指标命名及权重'})
        else:
            return JsonResponse({'message': '上传成功'})
    except:
        return JsonResponse({'message': '表格填写格式问题！'})


def upload_indicator(request):
    if request.method == 'GET':
        return render(request, 'standard/standard.html')
    elif request.method == 'POST':
        get_eval_name = request.GET.get('current_eval')
        get_admin_name = request.GET.get('current_admin')
        obj = request.FILES.get('file_obj_indicator')
        obj.name = time.strftime("%Y%m%d_%H_%M_%S_", time.localtime(time.time())) + obj.name
        # print(obj)
        if str(obj).endswith('.xlsx'):
            f = open(os.path.join('DESP', 'uploads', 'indicator', obj.name), 'wb')  ##存储位置
            for chunk in obj.chunks():
                f.write(chunk)
            f.close()
            return excel_import_indicator(obj, get_eval_name, get_admin_name)
        else:
            return JsonResponse({'message': '文件格式错误！'})


def download_indicator(request):
    # pdb.set_trace()
    file = open('DESP/uploads/indicator/TableIndicator_Import.xlsx', 'rb')
    response = HttpResponse(file)
    response['Content-Type'] = 'application/octet-stream'  # 设置头信息，告诉浏览器这是个文件
    response['Content-Disposition'] = 'attachment;filename="TableIndicator_Import.xlsx"'
    return response


def questionaire(request):
    a = request.GET.get('nodeID')
    print(a)
    questionlist = TableQuestionContent.objects.filter(table_question_content_col_indicator_id=a).order_by(
        'table_question_content_col_question_number')
    administrator = request.session['user_name']
    evalname = TableEvaluation.objects.filter(
        Q(table_evaluation_col_administrator=administrator) & Q(table_evaluation_col_status='启用')).values(
        'table_evaluation_col_name')
    current_eval = TableEvaluationIndicator.objects.filter(
        Q(table_evaluation_indicator_col_id=a)).values('table_evaluation_indicator_col_evaluation_name')
    current = current_eval[0]['table_evaluation_indicator_col_evaluation_name']
    print(administrator)
    data = [
        {
            'question_type': x.table_question_content_col_question_type,
            'indicator_id': x.table_question_content_col_indicator_id,
            'question_number': x.table_question_content_col_question_number,
            'marks': x.table_question_content_col_marks,
            'content': x.table_question_content_col_content,
            # 'scheme': x.table_question_content_col_mark_scheme,
            'markmethod': x.table_question_content_col_markmethod,
            'attachment': x.table_question_content_col_question_attachment,
            'class': x.table_question_content_col_question_class,
            'import': x.table_question_content_col_question_importanswer,
            'required': x.table_question_content_col_question_required
        } for x in questionlist
    ]
    # question = TableQuestionContent.objects.all()
    # for q in question:
    #     indicator = q.table_question_content_col_indicator_id
    #     eval = TableEvaluationIndicator.objects.filter(table_evaluation_indicator_col_id=indicator).values_list('table_evaluation_indicator_col_evaluation_name')[0][0]
    #     evalid = TableEvaluation.objects.get(table_evaluation_col_name=eval)
    #     q.table_question_content_col_evalname= evalid
    #     q.save()
    for question in data:
        for key in question:
            if question[key] == None:
                question[key] = ''
    return render(request, 'standard/questionaire.html',
                  {'data': data, 'evalname': evalname, 'admin': administrator, 'id': a, 'current_eval': current})


def choice_add(request):
    print(request.POST)
    if 'required' in request.POST:
        required = 'on'
    else:
        required = 'off'
    if 'attachment' in request.POST:
        attachment = 'on'
    else:
        attachment = 'off'
    if 'importanswer' in request.POST:
        importanswer = 'on'
    else:
        importanswer = 'off'
    data = {}
    data['title'] = request.POST['choicetitle']
    data['answer'] = request.POST.getlist('choice')
    existquestion = TableQuestionContent.objects.filter(
        table_question_content_col_indicator_id=request.POST['indicatorID']).values_list(
        'table_question_content_col_question_number')
    list = []
    for i in range(0, len(existquestion)):
        list.append(existquestion[i][0])
    indicator = TableEvaluationIndicator.objects.filter(
        table_evaluation_indicator_col_id=request.POST['indicatorID'])
    evalname = indicator.values_list('table_evaluation_indicator_col_evaluation_name')[0][0]
    evalname_object = TableEvaluation.objects.get(table_evaluation_col_name=evalname)
    if int(request.POST['questionnumber']) in list:
        question = {
            "table_question_content_col_question_type": request.POST['questiontype'],
            "table_question_content_col_question_class": request.POST['class'],
            "table_question_content_col_question_required": required,
            "table_question_content_col_question_attachment": attachment,
            "table_question_content_col_indicator_id": request.POST['indicatorID'],
            "table_question_content_col_question_number": request.POST['questionnumber'],
            'table_question_content_col_question_importanswer': importanswer,
            'table_question_content_col_markmethod': request.POST['markmethod'],
            'table_question_content_col_marks': request.POST['points'],
            'table_question_content_col_content': json.dumps(data, ensure_ascii=False),
            'table_question_content_col_evalname': evalname_object
        }
        TableQuestionContent.objects.filter(
            Q(table_question_content_col_indicator_id=request.POST['indicatorID']) & Q(
                table_question_content_col_question_number=request.POST['questionnumber'])).update(**question)
        return JsonResponse({'msg': 'success'})
    else:
        question = {
            "table_question_content_col_question_type": request.POST['questiontype'],
            "table_question_content_col_question_class": request.POST['class'],
            "table_question_content_col_question_required": required,
            "table_question_content_col_question_attachment": attachment,
            "table_question_content_col_indicator_id": request.POST['indicatorID'],
            "table_question_content_col_question_number": request.POST['questionnumber'],
            'table_question_content_col_question_importanswer': importanswer,
            'table_question_content_col_markmethod': request.POST['markmethod'],
            'table_question_content_col_marks': request.POST['points'],
            'table_question_content_col_content': json.dumps(data, ensure_ascii=False),
            'table_question_content_col_mark_scheme': None,
            'table_question_content_col_evalname': evalname_object
        }
        TableQuestionContent.objects.create(**question)
        return JsonResponse({'msg': 'success'})


def blank_add(request):
    if 'required' in request.POST:
        required = 'on'
    else:
        required = 'off'
    if 'attachment' in request.POST:
        attachment = 'on'
    else:
        attachment = 'off'
    if 'importanswer' in request.POST:
        importanswer = 'on'
    else:
        importanswer = 'off'
    indicator = TableEvaluationIndicator.objects.filter(
        table_evaluation_indicator_col_id=request.POST['indicatorID'])
    evalname = indicator.values_list('table_evaluation_indicator_col_evaluation_name')[0][0]
    evalname_object = TableEvaluation.objects.get(table_evaluation_col_name=evalname)
    data = {}
    data['title'] = request.POST['choicetitle']
    existquestion = TableQuestionContent.objects.filter(
        table_question_content_col_indicator_id=request.POST['indicatorID']).values_list(
        'table_question_content_col_question_number')
    list = []
    for i in range(0, len(existquestion)):
        list.append(existquestion[i][0])
    if int(request.POST['questionnumber']) in list:
        question = {
            "table_question_content_col_question_type": request.POST['questiontype'],
            "table_question_content_col_question_class": '',
            "table_question_content_col_question_required": required,
            "table_question_content_col_question_attachment": attachment,
            "table_question_content_col_indicator_id": request.POST['indicatorID'],
            "table_question_content_col_question_number": request.POST['questionnumber'],
            'table_question_content_col_question_importanswer': importanswer,
            'table_question_content_col_markmethod': request.POST['markmethod'],
            'table_question_content_col_marks': request.POST['points'],
            'table_question_content_col_content': json.dumps(data, ensure_ascii=False),
            'table_question_content_col_evalname': evalname_object
        }
        TableQuestionContent.objects.filter(
            Q(table_question_content_col_indicator_id=request.POST['indicatorID']) & Q(
                table_question_content_col_question_number=request.POST['questionnumber'])).update(**question)
        return JsonResponse({'msg': 'success'})
    else:
        question = {
            "table_question_content_col_question_type": request.POST['questiontype'],
            "table_question_content_col_question_class": '',
            "table_question_content_col_question_required": required,
            "table_question_content_col_question_attachment": attachment,
            "table_question_content_col_indicator_id": request.POST['indicatorID'],
            "table_question_content_col_question_number": request.POST['questionnumber'],
            'table_question_content_col_question_importanswer': importanswer,
            'table_question_content_col_markmethod': request.POST['markmethod'],
            'table_question_content_col_marks': request.POST['points'],
            'table_question_content_col_content': json.dumps(data, ensure_ascii=False),
            'table_question_content_col_mark_scheme': None,
            'table_question_content_col_evalname': evalname_object
        }
        TableQuestionContent.objects.create(**question)
        return JsonResponse({'msg': 'success'})


def answer_add(request):
    if 'required' in request.POST:
        required = 'on'
    else:
        required = 'off'
    if 'attachment' in request.POST:
        attachment = 'on'
    else:
        attachment = 'off'
    if 'importanswer' in request.POST:
        importanswer = 'on'
    else:
        importanswer = 'off'
    indicator = TableEvaluationIndicator.objects.filter(
        table_evaluation_indicator_col_id=request.POST['indicatorID'])
    evalname = indicator.values_list('table_evaluation_indicator_col_evaluation_name')[0][0]
    evalname_object = TableEvaluation.objects.get(table_evaluation_col_name=evalname)
    data = {}
    data['title'] = request.POST['choicetitle']
    existquestion = TableQuestionContent.objects.filter(
        table_question_content_col_indicator_id=request.POST['indicatorID']).values_list(
        'table_question_content_col_question_number')
    list = []
    for i in range(0, len(existquestion)):
        list.append(existquestion[i][0])
    if int(request.POST['questionnumber']) in list:
        question = {
            "table_question_content_col_question_type": request.POST['questiontype'],
            "table_question_content_col_question_class": request.POST['height'],
            "table_question_content_col_question_required": required,
            "table_question_content_col_question_attachment": attachment,
            "table_question_content_col_indicator_id": request.POST['indicatorID'],
            "table_question_content_col_question_number": request.POST['questionnumber'],
            'table_question_content_col_question_importanswer': importanswer,
            'table_question_content_col_markmethod': request.POST['markmethod'],
            'table_question_content_col_marks': request.POST['points'],
            'table_question_content_col_content': json.dumps(data, ensure_ascii=False),
            'table_question_content_col_mark_scheme': None,
            'table_question_content_col_evalname': evalname_object
        }
        TableQuestionContent.objects.filter(
            Q(table_question_content_col_indicator_id=request.POST['indicatorID']) & Q(
                table_question_content_col_question_number=request.POST['questionnumber'])).update(**question)
        return JsonResponse({'msg': 'success'})
    else:
        question = {
            "table_question_content_col_question_type": request.POST['questiontype'],
            "table_question_content_col_question_class": request.POST['height'],
            "table_question_content_col_question_required": required,
            "table_question_content_col_question_attachment": attachment,
            "table_question_content_col_indicator_id": request.POST['indicatorID'],
            "table_question_content_col_question_number": request.POST['questionnumber'],
            'table_question_content_col_question_importanswer': importanswer,
            'table_question_content_col_markmethod': request.POST['markmethod'],
            'table_question_content_col_marks': request.POST['points'],
            'table_question_content_col_content': json.dumps(data, ensure_ascii=False),
            'table_question_content_col_mark_scheme': None,
            'table_question_content_col_evalname': evalname_object
        }
        TableQuestionContent.objects.create(**question)
        return JsonResponse({'msg': 'success'})


def matrix_add(request):
    if 'required' in request.POST:
        required = 'on'
    else:
        required = 'off'
    if 'attachment' in request.POST:
        attachment = 'on'
    else:
        attachment = 'off'
    if 'importanswer' in request.POST:
        importanswer = 'on'
    else:
        importanswer = 'off'
    data = {}
    data['title'] = request.POST['choicetitle']
    data['column'] = request.POST.getlist('choice')
    data['rows'] = str(request.POST['row']).splitlines()
    indicator = TableEvaluationIndicator.objects.filter(
        table_evaluation_indicator_col_id=request.POST['indicatorID'])
    evalname = indicator.values_list('table_evaluation_indicator_col_evaluation_name')[0][0]
    evalname_object = TableEvaluation.objects.get(table_evaluation_col_name=evalname)
    existquestion = TableQuestionContent.objects.filter(
        table_question_content_col_indicator_id=request.POST['indicatorID']).values_list(
        'table_question_content_col_question_number')
    list = []
    for i in range(0, len(existquestion)):
        list.append(existquestion[i][0])
    if int(request.POST['questionnumber']) in list:
        question = {
            "table_question_content_col_question_type": request.POST['questiontype'],
            "table_question_content_col_question_class": request.POST['class'],
            "table_question_content_col_question_required": required,
            "table_question_content_col_question_attachment": attachment,
            "table_question_content_col_indicator_id": request.POST['indicatorID'],
            "table_question_content_col_question_number": request.POST['questionnumber'],
            'table_question_content_col_question_importanswer': importanswer,
            'table_question_content_col_markmethod': request.POST['markmethod'],
            'table_question_content_col_marks': request.POST['points'],
            'table_question_content_col_content': json.dumps(data, ensure_ascii=False),
            'table_question_content_col_mark_scheme': None,
            'table_question_content_col_evalname': evalname_object
        }
        TableQuestionContent.objects.filter(
            Q(table_question_content_col_indicator_id=request.POST['indicatorID']) & Q(
                table_question_content_col_question_number=request.POST['questionnumber'])).update(**question)
        return JsonResponse({'msg': 'success'})
    else:
        question = {
            "table_question_content_col_question_type": request.POST['questiontype'],
            "table_question_content_col_question_class": request.POST['class'],
            "table_question_content_col_question_required": required,
            "table_question_content_col_question_attachment": attachment,
            "table_question_content_col_indicator_id": request.POST['indicatorID'],
            "table_question_content_col_question_number": request.POST['questionnumber'],
            'table_question_content_col_question_importanswer': importanswer,
            'table_question_content_col_markmethod': request.POST['markmethod'],
            'table_question_content_col_marks': request.POST['points'],
            'table_question_content_col_content': json.dumps(data, ensure_ascii=False),
            'table_question_content_col_mark_scheme': None,
            'table_question_content_col_evalname': evalname_object
        }
        TableQuestionContent.objects.create(**question)
        return JsonResponse({'msg': 'success'})


def form_add(request):
    print(request.POST)
    if 'required' in request.POST:
        required = 'on'
    else:
        required = 'off'
    if 'attachment' in request.POST:
        attachment = 'on'
    else:
        attachment = 'off'
    if 'importanswer' in request.POST:
        importanswer = 'on'
    else:
        importanswer = 'off'
    indicator = TableEvaluationIndicator.objects.filter(
        table_evaluation_indicator_col_id=request.POST['indicatorID'])
    evalname = indicator.values_list('table_evaluation_indicator_col_evaluation_name')[0][0]
    evalname_object = TableEvaluation.objects.get(table_evaluation_col_name=evalname)
    data = {}
    data['title'] = request.POST['choicetitle']
    data['column'] = str(request.POST['column']).splitlines()
    data['rows'] = str(request.POST['row']).splitlines()
    existquestion = TableQuestionContent.objects.filter(
        table_question_content_col_indicator_id=request.POST['indicatorID']).values_list(
        'table_question_content_col_question_number')
    list = []
    for i in range(0, len(existquestion)):
        list.append(existquestion[i][0])
    if int(request.POST['questionnumber']) in list:
        question = {
            "table_question_content_col_question_type": request.POST['questiontype'],
            "table_question_content_col_question_class": '',
            "table_question_content_col_question_required": required,
            "table_question_content_col_question_attachment": attachment,
            "table_question_content_col_indicator_id": request.POST['indicatorID'],
            "table_question_content_col_question_number": request.POST['questionnumber'],
            'table_question_content_col_question_importanswer': importanswer,
            'table_question_content_col_markmethod': request.POST['markmethod'],
            'table_question_content_col_marks': request.POST['points'],
            'table_question_content_col_content': json.dumps(data, ensure_ascii=False),
            'table_question_content_col_mark_scheme': None,
            'table_question_content_col_evalname': evalname_object
        }
        TableQuestionContent.objects.filter(
            Q(table_question_content_col_indicator_id=request.POST['indicatorID']) & Q(
                table_question_content_col_question_number=request.POST['questionnumber'])).update(**question)
        return JsonResponse({'msg': 'success'})
    else:
        question = {
            "table_question_content_col_question_type": request.POST['questiontype'],
            "table_question_content_col_question_class": '',
            "table_question_content_col_question_required": required,
            "table_question_content_col_question_attachment": attachment,
            "table_question_content_col_indicator_id": request.POST['indicatorID'],
            "table_question_content_col_question_number": request.POST['questionnumber'],
            'table_question_content_col_question_importanswer': importanswer,
            'table_question_content_col_markmethod': request.POST['markmethod'],
            'table_question_content_col_marks': request.POST['points'],
            'table_question_content_col_content': json.dumps(data, ensure_ascii=False),
            'table_question_content_col_mark_scheme': None,
            'table_question_content_col_evalname': evalname_object
        }
        TableQuestionContent.objects.create(**question)
        return JsonResponse({'msg': 'success'})


def accumulation(request):
    print(request.POST)
    indicatorID = request.POST['indicatorID']
    questionnumber = request.POST['questionnumber']
    scheme = request.POST['datalist']
    markmethod = request.POST['markmethod']
    questiontype = request.POST['questiontype']
    if TableQuestionContent.objects.filter(Q(table_question_content_col_indicator_id=indicatorID) & Q(
            table_question_content_col_question_number=questionnumber)).exists():
        print(TableQuestionContent.objects.filter(Q(table_question_content_col_indicator_id=indicatorID) & Q(
            table_question_content_col_question_number=questionnumber)))
        TableQuestionContent.objects.filter(Q(table_question_content_col_indicator_id=indicatorID) & Q(
            table_question_content_col_question_number=questionnumber)).update(
            table_question_content_col_mark_scheme=scheme, table_question_content_col_markmethod=markmethod,
            table_question_content_col_question_type=questiontype)
    else:
        TableQuestionContent.objects.filter(Q(table_question_content_col_indicator_id=indicatorID) & Q(
            table_question_content_col_question_number=questionnumber)).create(
            table_question_content_col_mark_scheme=scheme, table_question_content_col_indicator_id=indicatorID,
            table_question_content_col_question_number=questionnumber,
            table_question_content_col_markmethod=markmethod,
            table_question_content_col_question_type=questiontype)
    return JsonResponse({'msg': 'success'})


def questionaire_manage(request):
    current_eval = request.GET.get('timeevalname')
    current_eval1 = current_eval
    # print(current_eval1)
    administrator = request.session['user_name']
    evalname = TableEvaluation.objects.filter(
        Q(table_evaluation_col_administrator=administrator) & Q(table_evaluation_col_name=current_eval))
    # print(evalname)
    eval_data = [
        {
            # 'org_id': TableOrganization.objects.filter(
            #     Q(table_organization_col_name=project.table_evaluation_col_organization)).values_list(
            #     'table_organization_col_id')[0][0],
            'org_name': project.table_evaluation_col_organization,
            'project_name': project.table_evaluation_col_name,
            'project_admin': project.table_evaluation_col_administrator,
            'questionaire_status': project.table_evaluation_col_status,
        } for project in evalname
    ]
    # print(eval_data)
    name_ind = []
    name = ''
    for each in eval_data:
        # print(each)
        if each['project_name'] == current_eval:
            # print(current_eval)
            for each1 in each['org_name']:
                if each1 != ',':
                    name += each1
                else:
                    # print(name,'\n')
                    name_ind.append(name)
                    name = ''
                if len(name) == len(each['org_name']):
                    # print(name, '\n')
                    name_ind.append(name)
                    name = ''

    # print(name_ind)
    orgnames = []
    orgnames1 = []
    for each in name_ind:
        orgnames.append(
            TableOrganization.objects.filter(
                Q(table_organization_col_id=int(each))
            )
        )
    # print(orgnames)
    for each in orgnames:
        for each1 in each:
            # print(each1.table_organization_col_name)
            orgnames1.append(each1.table_organization_col_name)
    # print(orgnames1)
    o = TableOrganization.objects.all()
    if o.exists():
        _data = [
            {
                'id': x.table_organization_col_id,
                'name': x.table_organization_col_name,
                'pId': x.table_organization_col_parent_name.table_organization_col_id if x.table_organization_col_parent_name else 0,
                'open': 1,
            } for x in o
        ]
    # print(evalname.table_evaluation_col_name)
    # timeevalname = models.TableTimeliner.objects.values('table_timeliner_col_evaluation').distinct().order_by(
    #     'table_timeliner_col_evaluation')
    # print(eval_data)
    return render(request, 'standard/manage.html',
                  {'name': name_ind, 'data': _data, 'current_eval': current_eval, 'current_eval1': current_eval1,
                   'eval_data': eval_data, 'orgnames': orgnames1,
                   'evalname': evalname, 'admin': administrator})


def questionaire_submit(request):
    print(request.POST)
    if request.POST['questiontype'] == '选择题':
        choice_add(request)
    elif request.POST['questiontype'] == '填空题':
        blank_add(request)
    elif request.POST['questiontype'] == '简答题':
        answer_add(request)
    elif request.POST['questiontype'] == '矩阵题':
        matrix_add(request)
    elif request.POST['questiontype'] == '表格题':
        form_add(request)
    return JsonResponse({'msg': 'success'})


def question_delete(request):
    print(request.POST)
    index = request.POST['index']
    nodeID = request.POST['nodeID']
    TableQuestionContent.objects.filter(Q(table_question_content_col_indicator_id=nodeID) & Q(
        table_question_content_col_question_number=index)).delete()
    length = TableQuestionContent.objects.filter(Q(table_question_content_col_indicator_id=nodeID)).count()
    list = []
    for i in range(0, length):
        list.append(i + 1)
    for obj, questionnumber in zip(
            TableQuestionContent.objects.filter(Q(table_question_content_col_indicator_id=nodeID)).order_by(
                'table_question_content_col_question_number'), list):
        obj.table_question_content_col_question_number = questionnumber
        obj.save()
    return JsonResponse({'msg': '删除成功！'})


def questionaire_delete(request):
    nodeID = request.POST['nodeID']
    TableQuestionContent.objects.filter(table_question_content_col_indicator_id=nodeID).delete()
    return JsonResponse({'msg': '删除成功!'})


def scheme_show(request):
    indicatorID = request.POST['indicatorID']
    questionnumber = request.POST['questionnumber']
    if TableQuestionContent.objects.filter(Q(table_question_content_col_indicator_id=indicatorID) & Q(
            table_question_content_col_question_number=questionnumber)).exists():
        scheme = TableQuestionContent.objects.filter(Q(table_question_content_col_indicator_id=indicatorID) & Q(
            table_question_content_col_question_number=questionnumber))
        markmethod = TableQuestionContent.objects.filter(Q(table_question_content_col_indicator_id=indicatorID) & Q(
            table_question_content_col_question_number=questionnumber)).values_list(
            'table_question_content_col_markmethod')[0][0]
        data = serializers.serialize('json', scheme)
        return JsonResponse({'data': data, 'msg': 'Created', 'markmethod': markmethod})
    else:
        return JsonResponse({'msg': 'Notcreatedyet'})


def export_answer(request):  # 导出答案部分
    pass


def import_answer(request):  # 导入答案部分
    org_dasdad = request.GET.get('adas')
    pass


def questionaire_status(request):
    org_name = request.GET.get('evalname')
    status = request.GET.get('status')
    pass


def calculate(request):
    # pdb.set_trace()
    current_eval = request.GET.get('timeevalname')
    administrator = request.session['user_name']
    evalname = TableEvaluation.objects.filter(
        Q(table_evaluation_col_administrator=administrator) & Q(table_evaluation_col_status='启用')).values(
        'table_evaluation_col_name')
    timeevalname = models.TableTimeliner.objects.values('table_timeliner_col_evaluation').distinct().order_by(
        'table_timeliner_col_evaluation')
    timeline_list = models.TableTimeliner.objects.filter(
        table_timeliner_col_evaluation=request.GET.get('timeevalname')).order_by('table_timeliner_col_start')
    dateline_list = models.TableTimeliner.objects.filter(
        table_timeliner_col_evaluation=request.GET.get('timeevalname')).order_by('table_timeliner_col_start')
    date_length = len(dateline_list)
    order_list = []
    order_count = 0
    while order_count < date_length:
        order_list.append(dateline_list.values_list('table_timeliner_col_id')[order_count][0])
        order_count = order_count + 1
    dateline = models.TableTimeliner.objects.filter(pk__in=order_list)
    for date in dateline:
        date_start = date.table_timeliner_col_start
        date_new_start = str(date_start).replace('-', '/')
        date_use_start = date_new_start[-2:] + date_new_start[4:8] + date_new_start[0:4]
        date.table_timeliner_col_start = date_use_start
        date_end = date.table_timeliner_col_end
        date_new_end = str(date_end).replace('-', '/')
        date_use_end = date_new_end[-2:] + date_new_end[4:8] + date_new_end[0:4]
        date.table_timeliner_col_end = date_use_end

    org_eval = models.TableEvaluation.objects.all()
    list1 = []
    list2 = []
    list3 = []
    res = []
    for x in org_eval:
        for each in timeline_list:
            if each.table_timeliner_col_evaluation == x.table_evaluation_col_name:
                list1.append(each.table_timeliner_col_end)
                list2.append(each)
        if len(list2) != 0:
            for each in list1:
                i = 0
                tmp = 0
                while i < 10:
                    if each[i] != '-':
                        tmp = int(each[i]) + tmp * 10
                    i += 1
                list3.append(tmp)
            res.append(list2[list3.index(max(list3))])
            list1 = []
            list2 = []
            list3 = []

    return render(request, 'standard/calculate.html',
                  {'evalname': evalname, 'admin': administrator, 'timeevalname': timeevalname,
                   'current_eval': current_eval,
                   'timeline_list': timeline_list, 'dateline': dateline, 'org_eval': org_eval,
                   'timeline_list': res})


def review(request):
    current_eval = request.GET.get('timeevalname')
    administrator = request.session['user_name']
    return render(request, 'standard/review.html', {'admin': administrator, 'current_eval': current_eval})
