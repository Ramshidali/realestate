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
from main.decorators import role_required
from main.functions import encrypt_message, generate_form_errors, paginate, randomnumber
from property.models import Unit
from tenant.forms import TenantForm, TenantDocumentForm, TenantUnitAssignForm
from tenant.models import Tenant, TenantDocuments, TenantUnitAssignment

# Create your views here.
@login_required
@role_required(['superadmin','admin_user'])
def tenant_list(request):
    """
    tenant listings
    :param request:
    :return: tenant list view
    """
    instances = Tenant.objects.filter(is_deleted=False).order_by("-id")
    
    filter_data = {}
    query = request.GET.get("q")
    
    if query:

        instances = instances.filter(
            Q(auto_id__icontains=query) |
            Q(name__icontains=query)
        )
        title = "Tenants - %s" % query
        filter_data['q'] = query
          

    context = {
        'instances': instances,
        'page_name' : 'Tenants',
        'page_title' : 'Tenants',
        'filter_data' : filter_data
    }

    return render(request, 'admin_panel/pages/tenant/tenant_list.html', context)

@login_required
@role_required(['superadmin','admin_user'])
def tenant_info(request,pk):
    """
    tenant single view using tenant pk
    :param request:
    :pk
    :return: tenant list view
    """
    instance = Tenant.objects.get(pk=pk, is_deleted=False)
    documents = TenantDocuments.objects.filter(tenant=instance,is_deleted=False)
    
    context = {
        'instance': instance,
        'documents' : documents,
        'page_name' : 'Tenant Details',
        'page_title' : 'Tenant Details',
        'is_need_light_box' : True,
    }

    return render(request, 'admin_panel/pages/tenant/tenant_info.html', context)


@login_required
@role_required(['superadmin','admin_user'])
def create_tenant(request):
    """
    create operation of tenant
    :param request:
    :return:
    """
    # check pk for getting instance    
    unitsFormset = formset_factory(TenantDocumentForm, extra=2)
    
    message = ''
    if request.method == 'POST':
        form = TenantForm(request.POST,files=request.FILES)
        tenant_document_formset = unitsFormset(request.POST,request.FILES,prefix='tenant_document_formset', form_kwargs={'empty_permitted': False})
        
        if form.is_valid() and tenant_document_formset.is_valid():
            try:
                with transaction.atomic():
                    #create tenant
                    data = form.save(commit=False)
                    data.save()
                    
                    if tenant_document_formset.is_valid():
                        for form in tenant_document_formset:
                            u_data = form.save(commit=False)
                            u_data.tenant = data
                            u_data.save()
                    
                    response_data = {
                        "status": "true",
                        "title": "Successfully Created",
                        "message": "tenant created successfully.",
                        'redirect': 'true',
                        "redirect_url": reverse('tenant:tenant_list')
                    }
                    
            except IntegrityError as e:
                # Handle database integrity error
                response_data = {
                    "status": "false",
                    "title": "Failed",
                    "message": "Integrity error occurred. Please check your data.",
                }

            except Exception as e:
                # Handle other exceptions
                response_data = {
                    "status": "false",
                    "title": "Failed",
                    "message": str(e),
                }
        else:
            message = generate_form_errors(form,tenant_document_formset, formset=True)
            
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:
        form = TenantForm()
        tenant_document_formset = unitsFormset(prefix='tenant_document_formset')

        context = {
            'form': form,
            'tenant_document_formset': tenant_document_formset,
            
            'page_name' : 'Create Tenant',
            'page_title' : 'Create Tenant',
            'is_need_select2' : True,
            'url' : reverse('tenant:create_tenant'),
        }

        return render(request, 'admin_panel/pages/tenant/create_tenant.html',context)


@login_required
@role_required(['superadmin','admin_user'])
def edit_tenant(request,pk):
    """
    edit operation of tenant
    :param request:
    :param pk:
    :return:
    """
    tenant_instance = get_object_or_404(Tenant, pk=pk)
    tenant_documents_instances = TenantDocuments.objects.filter(tenant=tenant_instance,is_deleted=False)
        
    if TenantDocuments.objects.filter(tenant=tenant_instance).exists():
        t_extra = 0
    else:
        t_extra = 1 

    UnitFormset = inlineformset_factory(
        Tenant,
        TenantDocuments,
        extra=t_extra,
        form=TenantDocumentForm,
    )
        
    message = ''
    
    if request.method == 'POST':
        form = TenantForm(request.POST,files=request.FILES,instance=tenant_instance)
        tenant_document_formset = UnitFormset(request.POST,request.FILES,
                                            instance=tenant_instance,
                                            prefix='tenant_document_formset',
                                            form_kwargs={'empty_permitted': False})            
        
        if form.is_valid() and tenant_document_formset.is_valid():
            
            #create tenant
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()
            
            #create multiple images
            if tenant_document_formset.is_valid():
                for form in tenant_document_formset:
                    if form not in tenant_document_formset.deleted_forms:
                        i_data = form.save(commit=False)
                        if not i_data.tenant :
                            i_data.tenant = data
                        i_data.save()

                for f in tenant_document_formset.deleted_forms:
                    f.instance.delete()
            
                response_data = {
                "status": "true",
                "title": "Successfully Updated",
                "message": "Tenant Updated Successfully.",
                'redirect': 'true',
                "redirect_url": reverse('tenant:tenant_list'),
                "return" : True,
            }

            else:
                response_data = {
                "status": "true",
                "title": "Successfully Updated",
                "message": "Tenant Updated successfully.",
                'redirect': 'true',
                "redirect_url": reverse('tenant:tenant_list'),
                "return" : False,
            }
    
        else:
            message = generate_form_errors(tenant_document_formset,formset=True)
            
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
                        
    else:

        form = TenantForm(instance=tenant_instance)
        tenant_document_formset = UnitFormset(queryset=tenant_documents_instances,
                                    prefix='tenant_document_formset',
                                    instance=tenant_instance)
        
        context = {
            'form': form,
            'tenant_document_formset': tenant_document_formset,
            'message': message,
            'tenant_instance': tenant_instance,
            'tenant_documents_instances': tenant_documents_instances,
            'page_name' : 'edit tenant',
            'url' : reverse('tenant:edit_tenant', args=[tenant_instance.pk]),            
        }

        return render(request, 'admin_panel/pages/tenant/create_tenant.html', context)


@login_required
@role_required(['superadmin','admin_user'])
def delete_tenant(request, pk):
    """
    tenant deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    Tenant.objects.filter(pk=pk).update(is_deleted=True)
    
    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Tenant Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('tenant:tenant_list')
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')