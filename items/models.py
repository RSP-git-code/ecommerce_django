from django.db import models
from  django.contrib.auth.models import User
# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=255)
    def __str__(self):
        return self.name 
    class Meta :
        ordering=('name',)
        verbose_name_plural="Categories"
class Item(models.Model):
    category=models.ForeignKey(Category,related_name='items',on_delete=models.CASCADE)
    name=models.CharField(max_length=255)
    description= models.TextField(blank=True,null=True)
    price=models.FloatField()
    image=models.ImageField(upload_to='item_images',blank=True,null=True)
    sold=models.BooleanField(default=False)
    created_by=models.ForeignKey(User,related_name='items',on_delete=models.CASCADE)
    date_time_created=models.DateTimeField(auto_now=True)