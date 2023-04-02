from django.db import models


class Member(models.Model):
    member_id = models.CharField(db_column='member_id',max_length=50)
    passwd = models.CharField(db_column='passwd', max_length=50)
    name = models.CharField(db_column='name', max_length=50)
    email = models.CharField(db_column='email', max_length=50, blank=True)
    usage_flag = models.CharField(db_column='usage_flag', max_length=10, default='y')
    reg_date = models.DateTimeField(db_column='reg_date', auto_now_add=True)
    update_date = models.DateTimeField(db_column='update_date', auto_now_add=True)

    class Meta:
#        managed = False
        db_table = 'member'

    def __str__(self):
        return '이름 : ' + self.name + ", 이메일 : " + self.email
