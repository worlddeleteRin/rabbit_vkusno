from django.db import models

# Create your models here.

class AccessToken(models.Model):
    token = models.CharField(max_length = 1000, default = None)
    
    def __str__(self):
        return self.token
