from django.db import models

# Create your models here.


class Shop(models.Model):
    title_tm = models.CharField(max_length=150)
    title_en = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20, blank=False, null=True)
    email = models.EmailField(blank=False, null=True)
    address_tm = models.CharField(max_length=300, blank=False)
    address_en = models.CharField(max_length=300, blank=False)
    
    def __str__(self):
        return self.title_tm
    
    

class Banner(models.Model):
    image_url = models.ImageField(upload_to='banner_images/', blank=True, null=True)
    
    
class Rule(models.Model):
    description_tm = models.TextField()
    description_en = models.TextField()