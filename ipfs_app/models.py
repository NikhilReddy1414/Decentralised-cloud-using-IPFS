from django.db import models

class File(models.Model):
    file_name = models.CharField(max_length=255 , default = 'Unknown')
    file_hash = models.CharField(max_length=46 , default = 'Unknown')
    username = models.CharField(max_length=255 , default = 'Unknown')

    def __str__(self):
        return self.file_name

class User(models.Model):
    username = models.CharField(max_length=255 , default = 'Unknown')
    password = models.CharField(max_length=255 , default = 'Unknown')
    peer_id = models.CharField(max_length=255 , default = 'Unknown')
    uc_tokens = models.FloatField(default = 100)

    def __str__(self):
        return self.username

# class wallet(models.Model):
#     username = models.CharField(max_length=255)
#     uc = models.IntegerField()

