#standerd
import json
import datetime
#django
from django.db.models import Q
from django.urls import reverse
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User,Group
from django.db import transaction, IntegrityError
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
#local
from admin_user.models import AdminUser
from main.decorators import role_required
from admin_user.forms import AdminUserForm
from main.functions import encrypt_message, generate_form_errors, paginate, randomnumber
from property.forms import PropertyForm, UnitForm
from property.models import Property, Unit
from tenant.forms import TenantUnitAssignForm
from tenant.models import TenantUnitAssignment

# Create your views here.
@login_required
@role_required(['superadmin','admin_user'])
def property_list(request):
    """
    property listings
    :param request:
    :return: property list view
    """
    instances = Property.objects.filter(is_deleted=False).order_by("-id")
    
    filter_data = {}
    query = request.GET.get("q")
    
    if query:

        instances = instances.filter(
            Q(auto_id__icontains=query) |
            Q(name__icontains=query)
        )
        title = "Properties - %s" % query
        filter_data['q'] = query
          

    context = {
        'instances': instances,
        'page_name' : 'Properties',
        'page_title' : 'Properties',
        'filter_data' : filter_data
    }

    return render(request, 'admin_panel/pages/property/property_list.html', context)

@login_required
@role_required(['superadmin','admin_user'])
def property_info(request,pk):
    """
    property single view using property pk
    :param request:
    :pk
    :return: property list view
    """
    instance = Property.objects.get(pk=pk, is_deleted=False)
    units = Unit.objects.filter(property=instance,is_deleted=False)
    assigned_tenants = TenantUnitAssignment.objects.filter(unit__property=instance)
    
    context = {
        'instance': instance,
        'units' : units,
        'assigned_tenants': assigned_tenants,
        'page_name' : 'Property Details',
        'page_title' : 'Property Details',
        'is_need_light_box' : True,
    }

    return render(request, 'admin_panel/pages/property/property_info.html', context)


@login_required
@role_required(['superadmin','admin_user'])
def create_property(request):
    """
    create operation of property
    :param request:
    :return:
    """
    # check pk for getting instance    
    unitsFormset = formset_factory(UnitForm, extra=2)
    
    message = ''
    if request.method == 'POST':
        form = PropertyForm(request.POST,files=request.FILES)
        units_formset = unitsFormset(request.POST,request.FILES,prefix='units_formset', form_kwargs={'empty_permitted': False})
        
        if form.is_valid() and units_formset.is_valid():
            #create property
            data = form.save(commit=False)
            data.save()
            
            if units_formset.is_valid():
                for form in units_formset:
                    u_data = form.save(commit=False)
                    u_data.property = data
                    u_data.save()
                    
            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "property created successfully.",
                'redirect': 'true',
                "redirect_url": reverse('property:property_list')
            }
    
        else:
            message = generate_form_errors(form,units_formset, formset=True)
            
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:
        form = PropertyForm()
        units_formset = unitsFormset(prefix='units_formset')

        context = {
            'form': form,
            'units_formset': units_formset,
            
            'page_name' : 'Create property',
            'page_title' : 'Create property',
            'is_need_select2' : True,
            'url' : reverse('property:create_property'),
        }

        return render(request, 'admin_panel/pages/property/create_property.html',context)


@login_required
@role_required(['superadmin','admin_user'])
def edit_property(request,pk):
    """
    edit operation of property
    :param request:
    :param pk:
    :return:
    """
    proprty_instance = get_object_or_404(Property, pk=pk)
    unit_instance = Unit.objects.filter(property=proprty_instance,is_deleted=False)
        
    if Unit.objects.filter(product=proprty_instance).exists():
        u_extra = 0
    else:
        u_extra = 1 

    UnitFormset = inlineformset_factory(
        Property,
        Unit,
        extra=u_extra,
        form=UnitForm,
    )
        
    message = ''
    
    if request.method == 'POST':
        form = PropertyForm(request.POST,files=request.FILES,instance=proprty_instance)
        units_formset = UnitFormset(request.POST,request.FILES,
                                                             instance=proprty_instance,
                                                             prefix='units_formset',
                                                             form_kwargs={'empty_permitted': False})            
        
        if form.is_valid() and units_formset.is_valid():
            
            #create product
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()
            
            #create multiple images
            if units_formset.is_valid():
                for form in units_formset:
                    if form not in units_formset.deleted_forms:
                        i_data = form.save(commit=False)
                        if not i_data.property :
                            i_data.property = data
                        i_data.save()

                for f in units_formset.deleted_forms:
                    f.instance.delete()
            
                response_data = {
                "status": "true",
                "title": "Successfully Updated",
                "message": "Property Updated Successfully.",
                'redirect': 'true',
                "redirect_url": reverse('product:property_list'),
                "return" : True,
            }

            else:
                response_data = {
                "status": "true",
                "title": "Successfully Updated",
                "message": "Property Updated successfully.",
                'redirect': 'true',
                "redirect_url": reverse('product:property_list'),
                "return" : False,
            }
    
        else:
            message = generate_form_errors(units_formset,formset=True)
            
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
                        
    else:

        form = PropertyForm(instance=proprty_instance)
        units_formset = UnitFormset(queryset=unit_instance,
                                    prefix='units_formset',
                                    instance=proprty_instance)
        
        context = {
            'form': form,
            'units_formset': units_formset,
            'message': message,
            'pro_instance': proprty_instance,
            'unit_instance': unit_instance,
            'page_name' : 'edit product',
            'url' : reverse('product:edit_property', args=[proprty_instance.pk]),            
        }

        return render(request, 'admin_panel/pages/property/create_property.html', context)


@login_required
@role_required(['superadmin','admin_user'])
def delete_property(request, pk):
    """
    property deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    Property.objects.filter(pk=pk).update(is_deleted=True)
    
    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Property Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('property:property_list')
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')

@login_required
@role_required(['superadmin','admin_user'])
def assign_property_tenant(request, unit_id):
    """
    assign property to tenant
    :param request:
    :return:
    """
    message = ''
    
    if request.method == 'POST':
        form = TenantUnitAssignForm(request.POST,files=request.FILES)
        unit_instance = get_object_or_404(Unit, pk=unit_id)
        
        if form.is_valid() :
            data = form.save(commit=False)
            data.unit = unit_instance
            data.save()
            
            response_data = {
                "status": "true",
                "title": "Successfully Assigned",
                "message": "property assigned successfully.",
                'redirect': 'true',
                "redirect_url": reverse('property:property_info', kwargs={'pk':unit_instance.property.pk})
            }
            
        else:
            message = generate_form_errors(form, formset=False)
            
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:
        form = TenantUnitAssignForm()

        context = {
            'form': form,
            
            'page_name' : 'Assign property to Tenant',
            'page_title' : 'Assign property to Tenant',
            'is_need_select2' : True,
            'url' : reverse('property:assign_property_tenant', kwargs={'unit_id': unit_id})
        }

        return render(request, 'admin_panel/pages/tenant/assign_tenant.html',context)