# Generated by Django 4.0.4 on 2022-05-19 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hostelmanagement', '0006_alter_hostel_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hostel',
            name='details',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='hostelmanagement.hosteldetail'),
            preserve_default=False,
        ),
    ]