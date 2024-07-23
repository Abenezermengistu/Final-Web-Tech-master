from django.db import models

# Create your models here.
class UserConnection(models.Model):
    user_ip = models.CharField(primary_key=True, max_length=50)
    num_conn = models.IntegerField(default=1) 
    
    def __str__(self):
        return self.user_ip