# Generated by Django 3.1 on 2022-08-09 06:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='useredit',
            old_name='Deleted_by',
            new_name='action',
        ),
        migrations.RenameField(
            model_name='useredit',
            old_name='client',
            new_name='userCode',
        ),
        migrations.RemoveField(
            model_name='useredit',
            name='lot',
        ),
        migrations.RemoveField(
            model_name='useredit',
            name='oTime',
        ),
        migrations.RemoveField(
            model_name='useredit',
            name='order_price',
        ),
        migrations.RemoveField(
            model_name='useredit',
            name='order_type',
        ),
        migrations.RemoveField(
            model_name='useredit',
            name='qty',
        ),
        migrations.RemoveField(
            model_name='useredit',
            name='symbol',
        ),
        migrations.RemoveField(
            model_name='useredit',
            name='tType',
        ),
    ]
