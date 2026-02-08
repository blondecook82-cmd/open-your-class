from django.db.models import Model, DateTimeField

class BaseTimeStamp(Model):
    date_pub = DateTimeField(auto_now_add=True)
    date_edit = DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True