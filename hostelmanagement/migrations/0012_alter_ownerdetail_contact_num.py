# Generated by Django 4.0.4 on 2022-08-04 18:08

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('hostelmanagement', '0011_rename_post_reviews_hostel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ownerdetail',
            name='contact_num',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None),
        ),
    ]