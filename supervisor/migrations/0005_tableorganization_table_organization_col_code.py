# Generated by Django 3.1.3 on 2020-12-22 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supervisor', '0004_remove_tableevaluation_table_organization_col_indicator_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='tableorganization',
            name='table_organization_col_code',
            field=models.CharField(blank=True, db_column='Table_Organization_col_Code', max_length=100, null=True, unique=True),
        ),
    ]
