from django.db import models


class Members(models.Model):
    name = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length=100, null=True)
    user_id = models.IntegerField(null=True)
    ROLES = ((1, "admin"), (2, "project member"))
    backlog_user_id = models.CharField(max_length=50, null=True)
    role_type = models.PositiveSmallIntegerField(choices=ROLES)
    STATUS_CHOICES = ((0, "inactive"), (1, "Active"))
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "members"
        
