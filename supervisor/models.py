from django.db import models
from login.models import TableUser


# Create your models here.
class TableOrganization(models.Model):
    table_organization_col_id = models.IntegerField(db_column='Table_Organization_col_id',
                                                    primary_key=True)  # Field name made lowercase.
    table_organization_col_name = models.CharField(db_column='Table_Organization_col_Name',

                                                   max_length=100,unique=True)  # Field name made lowercase.
    table_organization_col_code = models.CharField(db_column='Table_Organization_col_Code',
                                                   max_length=100, unique=True,blank=True,null=True)
    table_organization_col_address = models.CharField(db_column='Table_Organization_col_Address',
                                                      max_length=100, null=True)  # Field name made lowercase.
    table_organization_col_postcode = models.CharField(db_column='Table_Organization_col_Postcode',
                                                       max_length=20, null=True)  # Field name made lowercase.
    # table_organization_col_root = models.CharField(db_column='Table_Organization_col_Root',
    #                                                max_length=100)  # Field name made lowercase.
    table_organization_col_parent_name = models.ForeignKey('self', on_delete=models.CASCADE, db_constraint=False,
                                                           null=True, blank=True,
                                                           verbose_name='父机构')  # Field name made lowercase.
    # table_organization_col_type = models.CharField(db_column='Table_Organization_col_Type', max_length=50, blank=True,
    #                                                null=True)  # Field name made lowercase.
    table_organization_col_field = models.CharField(db_column='Table_Organization_col_Field', max_length=50, blank=True,
                                                    null=True)  # Field name made lowercase.
    # table_organization_col_unicode = models.CharField(db_column='Table_Organization_col_Unicode', max_length=50, null=True)

    class Meta:
        managed = True
        db_table = 'Table_Organization'


class TableEvaluation(models.Model):
    table_evaluation_col_id = models.IntegerField(db_column='Table_Evaluation_col_id',
                                                  primary_key=True)  # Field name made lowercase.
    table_evaluation_col_name = models.CharField(db_column='Table_Evaluation_col_Name',
                                                 max_length=50)  # Field name made lowercase.
    table_evaluation_col_administrator = models.CharField(db_column='Table_Evaluation_col_Administrator',
                                                          max_length=50)  # Field name made lowercase.
    table_evaluation_col_status = models.CharField(
        db_column='Table_Evaluation_col_Status', max_length=128)  # Field name made lowercase.
    table_evaluation_col_create_time = models.CharField(db_column='Table_Evaluation_col_Create_Time',
                                                        max_length=100)  # Field name made lowercase.
    table_evaluation_col_finish_time = models.CharField(db_column='Table_Evaluation_col_Finish_Time',
                                                        max_length=100)  # Field name made lowercase.
    table_evaluation_col_organization = models.CharField(db_column='Table_Evaluation_col_Organization',
                                                         max_length=50)  # Field name made lowercase.
    table_evaluation_col_deliver = models.CharField(db_column='Table_Evaluation_col_Deliver', max_length=50, null=True)
    table_evaluation_col_mark = models.CharField(db_column='Table_Evaluation_col_Mark', null=True, max_length=128)

    class Meta:
        managed = True
        db_table = 'Table_Evaluation'
