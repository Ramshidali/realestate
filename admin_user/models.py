import uuid

from django.db import models
from django.contrib.auth.models import User

from versatileimagefield.fields import VersatileImageField

# Create your models here.
class AdminUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    password = models.CharField(max_length=256,null=True,blank=True)
    image = VersatileImageField('Image', upload_to="admin_user/profile_pic", blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    
    user = models.OneToOneField(User,on_delete=models.CASCADE,blank=True,null=True)
    
    class Meta:
        db_table = 'admin_user'
        verbose_name = ('Admin User')
        verbose_name_plural = ('Admin User')
        
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    def get_fullname(self):
        return f'{self.first_name} {self.last_name}'
    
    def get_initial(self):
        first_name = self.first_name[0] if self.first_name else ''
        last_name = self.last_name[0] if self.last_name else ''
        return first_name.upper() + last_name.upper()