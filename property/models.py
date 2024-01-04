import uuid

from django.db import models
from django.contrib.auth.models import User

from decimal import Decimal
from ckeditor.fields import RichTextField
from versatileimagefield.fields import VersatileImageField

UNIT_TYPES = (
    ('010', '1BHK'),
    ('015', '2BHK'),
    ('020', '3BHK'),
    ('025', '4BHK'),
    ('030', '5BHK'),
    ('035', '6BHK'),
)

# Create your models here.
class Property(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    address = models.TextField()
    features = RichTextField()
    location = models.CharField(max_length=256)
    image = VersatileImageField('Image', upload_to="propertes/property", blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'properties'
        verbose_name = ('Property')
        verbose_name_plural = ('Property')
        
    def __str__(self):
        return str(self.id)

class Unit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=3, choices=UNIT_TYPES)
    rent_cost = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    main_image = VersatileImageField('Image', upload_to="units/main_images", blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'units'
        verbose_name = ('Unit')
        verbose_name_plural = ('Unit')
        
    def __str__(self):
        return str(self.id)