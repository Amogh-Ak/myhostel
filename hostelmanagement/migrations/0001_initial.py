# Generated by Django 4.0.4 on 2022-04-30 13:06

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_Owner', models.BooleanField(default=False, verbose_name='Owner')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Facilities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facility', models.CharField(max_length=70)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_number', models.IntegerField()),
                ('number_of_students', models.IntegerField()),
                ('status', models.CharField(choices=[('Available', 'Available'), ('Full', 'Full'), ('Not Available', 'Not Available')], max_length=100)),
                ('room_imgs', models.ImageField(upload_to='rooms')),
                ('room_cost', models.IntegerField()),
                ('usr', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OwnerDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('profilePic', models.ImageField(default=None, upload_to='ownerProfile')),
                ('address', models.CharField(max_length=200)),
                ('contact_num', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True)),
                ('usr', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HostelDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notice_period', models.IntegerField()),
                ('near_by', models.CharField(max_length=300)),
                ('visitors_allowed', models.BooleanField(default=False)),
                ('security_deposit', models.IntegerField()),
                ('warden', models.BooleanField()),
                ('restrictions', models.CharField(max_length=200)),
                ('usr', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Hostel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
                ('location', models.CharField(max_length=200)),
                ('zipcode', models.IntegerField()),
                ('type_of_hostel', models.CharField(choices=[('Mens Hostel', 'Mens Hostel'), ('Womens Hostel', 'Womens Hostel')], max_length=50)),
                ('food_facility', models.CharField(choices=[('With Mess', 'With Mess'), ('Without Mess', 'Without Mess')], default='With Food', max_length=50, null=True)),
                ('views', models.IntegerField(default=0)),
                ('description', models.TextField(max_length=1000)),
                ('images', models.ImageField(upload_to='hostelImage')),
                ('status', models.CharField(choices=[('Approved', 'Approved'), ('Rejected', 'Rejected'), ('On Hold', 'On Hold'), ('Suspended', 'Suspended')], default='Not Approved.', max_length=50)),
                ('details', models.ManyToManyField(to='hostelmanagement.hosteldetail')),
                ('facilities', models.ManyToManyField(to='hostelmanagement.facilities')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hostelmanagement.room')),
                ('usr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
