import uuid
from django.db import models

from decimal import Decimal
from versatileimagefield.fields import VersatileImageField

from property.models import Unit

DOCUMENT_TYPES = (
    ('010', 'Adhar Card'),
    ('015', 'Driving Licence'),
    ('020', 'Voter ID'),
    ('025', 'Passport'),
)

# Create your models here.
class Tenant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    address = models.TextField()
    image = VersatileImageField('Image', upload_to="propertes/property", blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'tenant'
        verbose_name = ('Tenant')
        verbose_name_plural = ('Tenant')
        
    def __str__(self):
        return str(self.name)
    
class TenantDocuments(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=3, choices=DOCUMENT_TYPES)
    document = models.FileField(upload_to="tenant/document")
    is_deleted = models.BooleanField(default=False)
    
    tenant = models.ForeignKey(Tenant,on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'tenant_documents'
        verbose_name = ('Tenant Documents')
        verbose_name_plural = ('Tenant Documents')
        
    def __str__(self):
        return str(self.id)
    
class TenantUnitAssignment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agreement_end_date = models.DateTimeField()
    monthly_rent_date = models.CharField(max_length=2)
    attachement = models.FileField(upload_to="tenant_unit/document",null=True,blank=True)
    is_deleted = models.BooleanField(default=False)
    
    tenant = models.ForeignKey(Tenant,on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit,on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'tenant_assigned_unit'
        verbose_name = ('Tenant Assigned Unit')
        verbose_name_plural = ('Tenant Assigned Unit')
        
    def __str__(self):
        return str(self.id)