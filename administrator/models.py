from django.db import models
from supervisor.models import TableEvaluation


class TableEvaluationIndicator(models.Model):
    table_evaluation_indicator_col_id = models.IntegerField(db_column='Table_Evaluation_Indicator_col_id',
                                                            primary_key=True)  # Field name made lowercase.
    table_evaluation_indicator_col_name = models.CharField(db_column='Table_Evaluation_Indicator_col_Name',
                                                           max_length=50)  # Field name made lowercase.
    # table_evaluation_indicator_col_root = models.CharField(db_column='Table_Evaluation_Indicator_col_Root',
    #                                                        max_length=50)  # Field name made lowercase.
    # table_evaluation_indicator_col_parent_id = models.IntegerField(db_column='Table_Evaluation_Indicator_col_Parent_id',
    #                                                                blank=True, null=True)  # Field name made lowercase.
    # table_evaluation_indicator_col_parent_name = models.CharField(
    #     db_column='Table_Evaluation_Indicator_col_Parent_Name', max_length=50, blank=True,
    #     null=True)  # Field name made lowercase.
    table_evaluation_indicator_col_parent_name = models.ForeignKey('self', on_delete=models.PROTECT, db_constraint=False,
                               null=True, blank=True, verbose_name='父部门')
    table_evaluation_indicator_col_weight = models.DecimalField(db_column='Table_Evaluation_Indicator_col_Weight',
                                                                max_digits=10,
                                                                decimal_places=2)  # Field name made lowercase.
    table_evaluation_indicator_col_evaluation_name = models.CharField(
        db_column='Table_Evaluation_Indicator_col_Evaluation_Name', max_length=50)  # Field name made lowercase.
    table_evaluation_indicator_col_administrator_id = models.IntegerField(
        db_column='Table_Evaluation_Indicator_col_Administrator_id')  # Field name made lowercase.
    table_evaluation_indicator_col_administrator_name = models.CharField(
        db_column='Table_Evaluation_Indicator_col_Administrator_Name', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Table_Evaluation_Indicator'


class TableQuestionaire(models.Model):
    table_questionaire_col_id = models.IntegerField(db_column='Table_Questionaire_col_id', primary_key=True)  # Field name made lowercase.
    table_questionaire_col_organization_id = models.CharField(db_column='Table_Questionaire_col_organization_id', max_length=50)  # Field name made lowercase.
    table_questionaire_col_organization_contact = models.CharField(db_column='Table_Questionaire_col_organization_contact', max_length=50)  # Field name made lowercase.
    table_questionaire_col_organization_email = models.CharField(db_column='Table_Questionaire_col_organization_email', max_length=50)  # Field name made lowercase.
    table_questionaire_col_indicator_id = models.CharField(db_column='Table_Questionaire_col_indicator_id', max_length=50)  # Field name made lowercase.
    table_questionaire_col_question_id = models.CharField(db_column='Table_Questionaire_col_question_id', unique=True, max_length=50)  # Field name made lowercase.
    table_questionaire_col_question_number = models.CharField(db_column='Table_Questionaire_col_question_number', max_length=50)  # Field name made lowercase.
    table_questionaire_col_question_content = models.CharField(db_column='Table_Questionaire_col_question_content', max_length=50)  # Field name made lowercase.
    table_questionaire_col_question_status = models.CharField(db_column='Table_Questionaire_col_question_status', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Table_Questionaire'


class TableQuestionContent(models.Model):
    table_question_content_col_question_id = models.AutoField(db_column='Table_Question_Content_col_Question_id', primary_key=True)  # Field name made lowercase.
    table_question_content_col_question_type = models.CharField(db_column='Table_Question_Content_col_Question_type', max_length=256,null=True)  # Field name made lowercase.
    table_question_content_col_question_class = models.CharField(db_column='Table_Question_Content_col_Question_class',max_length=256,
                                                                   null=True)  # Field name made lowercase.
    table_question_content_col_question_required = models.CharField(db_column='Table_Question_Content_col_Question_required',max_length=256,
                                                                   null=True)  # Field name made lowercase.
    table_question_content_col_question_attachment = models.CharField(db_column='Table_Question_Content_col_Question_attachment',max_length=256,
                                                                   null=True)  # Field name made lowercase.
    table_question_content_col_indicator_id = models.IntegerField(db_column='Table_Question_Content_col_Indicator_id',null=True)  # Field name made lowercase.
    table_question_content_col_question_number = models.IntegerField(db_column='Table_Question_Content_col_Question_number',null=True)  # Field name made lowercase.
    table_question_content_col_question_importanswer = models.CharField(db_column='Table_Question_Content_col_Question_Importanswer',max_length=256,
                                                                   null=True)  # Field name made lowercase.
    table_question_content_col_markmethod = models.CharField(db_column='Table_Question_Content_col_Markmethod',max_length=256,null=True)  # Field name made lowercase.
    table_question_content_col_marks = models.CharField(db_column='Table_Question_Content_col_Marks', max_length=50,null=True)  # Field name made lowercase.
    table_question_content_col_content = models.JSONField(db_column='Table_Question_Content_col_Content',max_length=256,null=True)  # Field name made lowercase.
    table_question_content_col_mark_scheme = models.JSONField(db_column='Table_Question_Content_col_Mark_scheme', max_length=256,
                                                                   null=True)  # Field name made lowercase.
    table_question_content_col_evalname = models.ForeignKey('supervisor.TableEvaluation',on_delete=models.CASCADE, db_constraint=False, null=True)

    class Meta:
        managed = True
        db_table = 'Table_Question_Content'

class TableTimeliner(models.Model):
    table_timeliner_col_id = models.AutoField(db_column='Table_Timeliner_col_id', primary_key=True)  # Field name made lowercase.
    table_timeliner_col_start = models.CharField(db_column='Table_Timeliner_col_start', max_length=128)  # Field name made lowercase.
    table_timeliner_col_content = models.CharField(db_column='Table_Timeliner_col_content', unique=True, max_length=255)  # Field name made lowercase.
    table_timeliner_col_end = models.CharField(db_column='Table_Timeliner_col_end', max_length=128)  # Field name made lowercase.
    table_timeliner_col_status = models.CharField(db_column='Table_Timeliner_col_status', max_length=128)  # Field name made lowercase.
    table_timeliner_col_name = models.CharField(db_column='Table_Timeliner_col_name', max_length=128)
    table_timeliner_col_evaluation = models.CharField(db_column='Table_Timeliner_col_evaluation', max_length=128)

    class Meta:
        managed = True
        db_table = 'Table_Timeliner'
        ordering = ['table_timeliner_col_start']


class TableQuestionResult(models.Model):
    table_question_result_col_id = models.AutoField(db_column='Table_Question_Result_col_id', primary_key=True)
    table_question_result_col_answer = models.CharField(db_column='Table_Question_Result_col_Answer', max_length=256, null=True)
    table_question_result_col_marks = models.CharField(db_column='Table_Question_Result_col_Marks', max_length=256, null=True)
    table_question_result_col_blank = models.CharField(db_column='Table_Question_Result_col_Blank', max_length=256, null=True)
    table_question_result_col_user_id = models.CharField(db_column='Table_Question_Result_col_user_id', max_length=256, null=True)
    table_question_result_col_questionaire_id = models.CharField(db_column='Table_Question_Result_col_questionaire_id', max_length=256, null=True)
    table_question_result_col_question_id = models.CharField(db_column='Table_Question_Result_col_question_id', max_length=256, null=True)

    class Meta:
        managed = True
        db_table = 'Table_Question_Result'


class TableUploadFile(models.Model):
    table_upload_file_col_id = models.AutoField(db_column='Table_Upload_File_col_id', primary_key=True)
    table_upload_file_col_name = models.CharField(db_column='Table_Upload_File_col_name', max_length=256)
    table_upload_file_col_time = models.CharField(db_column='Table_Upload_File_col_time', max_length=256)
    table_upload_file_col_evaluation = models.CharField(db_column='Table_Upload_File_col_evaluation', max_length=256)
    table_upload_file_col_timeliner = models.CharField(db_column='Table_Upload_File_col_timeliner', max_length=256)
    table_upload_file_col_cover = models.CharField(db_column='Table_Upload_File_col_cover', max_length=256)

    class Meta:
        managed = True
        db_table = 'Table_Upload_File'

