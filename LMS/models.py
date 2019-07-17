# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DailyTime(models.Model):
    id = models.CharField(primary_key=True, max_length=45)
    date = models.CharField(max_length=45, blank=True, null=True)
    start_time = models.CharField(max_length=45, blank=True, null=True)
    end_time = models.CharField(max_length=45, blank=True, null=True)
    uname = models.CharField(max_length=8, blank=True, null=True)
    time_length = models.CharField(max_length=45, blank=True, null=True)
    reason = models.CharField(max_length=200, blank=True, null=True)
    leave_time = models.CharField(max_length=8, blank=True, null=True)
    daily_timecol = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'daily_time'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class StudentTask(models.Model):
    sid = models.IntegerField(primary_key=True)
    sname = models.CharField(max_length=8, blank=True, null=True)
    uid = models.IntegerField(blank=True, null=True)
    uname = models.CharField(max_length=45, blank=True, null=True)
    tid = models.IntegerField(blank=True, null=True)
    content = models.CharField(max_length=80, blank=True, null=True)
    finish = models.CharField(max_length=8, blank=True, null=True)
    progress = models.IntegerField(blank=True, null=True)
    value = models.IntegerField(blank=True, null=True)
    duration = models.CharField(max_length=4, blank=True, null=True)
    start_time = models.DateField(blank=True, null=True)
    end_time = models.DateField(blank=True, null=True)
    path = models.CharField(max_length=800, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'student_task'


class Task(models.Model):
    tid = models.IntegerField(primary_key=True)
    tname = models.CharField(max_length=8, blank=True, null=True)
    content = models.CharField(max_length=80, blank=True, null=True)
    students = models.CharField(max_length=80, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    finish = models.CharField(max_length=8, blank=True, null=True)
    progress = models.IntegerField(blank=True, null=True)
    value = models.IntegerField(blank=True, null=True)
    duration = models.CharField(max_length=4, blank=True, null=True)
    start_time = models.DateField(blank=True, null=True)
    end_time = models.DateField(blank=True, null=True)
    path = models.CharField(max_length=800, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'task'


class Time(models.Model):
    date = models.IntegerField(primary_key=True)
    uid = models.IntegerField(blank=True, null=True)
    time_day = models.IntegerField(blank=True, null=True)
    time_week = models.IntegerField(blank=True, null=True)
    time_month = models.IntegerField(blank=True, null=True)
    apply = models.IntegerField(blank=True, null=True)
    reason_a = models.CharField(max_length=20, blank=True, null=True)
    leave = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'time'


class User(models.Model):
    uid = models.IntegerField(primary_key=True)
    uname = models.CharField(max_length=8, blank=True, null=True)
    password = models.CharField(max_length=10, blank=True, null=True)
    type = models.CharField(max_length=8, blank=True, null=True)
    room = models.CharField(max_length=8, blank=True, null=True)
    sex = models.CharField(max_length=2, blank=True, null=True)
    class_field = models.CharField(db_column='class', max_length=8, blank=True, null=True)  # Field renamed because it was a Python reserved word.
    birthday = models.CharField(max_length=8, blank=True, null=True)
    photo = models.CharField(max_length=20, blank=True, null=True)
    tel = models.CharField(max_length=11, blank=True, null=True)
    email = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'
