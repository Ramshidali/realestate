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
from django.shortcuts import get_object_or_404, redirect, render
#local
from admin_user.models import AdminUser
from main.decorators import role_required
from admin_user.forms import AdminUserForm
from main.functions import encrypt_message, generate_form_errors, paginate, randomnumber

# Create your views here.
@login_required
@role_required(['superadmin','admin_user'])
def admin_user_info(request,pk):
    """
    Admin User info
    :param request:
    :return: Admin User info view
    """
    instance = AdminUser.objects.get(pk=pk,is_deleted=False)

    context = {
        'instance': instance,
        'page_name' : 'Admin User',
        'page_title' : 'Admin User',
    }

    return render(request, 'admin_panel/pages/admin_user/user_info.html', context)

@login_required
@role_required(['superadmin','admin_user'])
def admin_user_list(request):
    """
    Admin User listings
    :param request:
    :return: Admin User list view
    """
    instances = AdminUser.objects.filter(is_deleted=False).order_by("-id")
    
    filter_data = {}
    query = request.GET.get("q")
    
    if query:

        instances = instances.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) 
        )
        title = "AdminUser - %s" % query
        filter_data['q'] = query

    context = {
        'instances': instances,
        'page_name' : 'Admin User',
        'page_title' : 'Admin User',
        'filter_data' :filter_data,
    }

    return render(request, 'admin_panel/pages/admin_user/user_list.html', context)

@login_required
@role_required(['superadmin','admin_user'])
def create_admin_user(request):
    """
    create operation of AdminUser
    :param request:
    :param pk:
    :return:
    """
    if request.method == 'POST':
        # if instance go to edit
        form = AdminUserForm(request.POST)
            
        if form.is_valid():
            try:
                with transaction.atomic():
                    
                    email = form.cleaned_data['email']
                    password = form.cleaned_data['password']
                    
                    user_data = User.objects.create_user(
                        username=email,
                        password=password,
                        is_active=True,
                    )
                    
                    if Group.objects.filter(name="admin_user").exists():
                        group = Group.objects.get(name="admin_user")
                    else:
                        group = Group.objects.create(name="admin_user")

                    user_data.groups.add(group)
                    
                    data = form.save(commit=False)
                    data.user = user_data
                    data.password = encrypt_message(password)
                    data.save()
                    
                    response_data = {
                        "status": "true",
                        "title": "Successfully Created",
                        "message": "Admin User created successfully.",
                        'redirect': 'true',
                        "redirect_url": reverse('admin_user:admin_user_list')
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
            message =generate_form_errors(form , formset=False)
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    
    else:
        
        form = AdminUserForm()

        context = {
            'form': form,
            'page_name' : 'Create Admin User',
            'page_title' : 'Create Admin User',
            'url' : reverse('admin_user:create_admin_user'),
            
            'is_need_datetime_picker': True,
            'is_need_forms': True,
        }

        return render(request, 'admin_panel/pages/create/create.html',context)
    
@login_required
@role_required(['superadmin','admin_user'])
def edit_admin_user(request,pk):
    """
    edit operation of admin_user
    :param request:
    :param pk:
    :return:
    """
    instance = get_object_or_404(AdminUser, pk=pk)
        
    message = ''
    if request.method == 'POST':
        form = AdminUserForm(request.POST,files=request.FILES,instance=instance)
        
        if form.is_valid():
            #update AdminUser
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()
            form.save_m2m()
                    
            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Admin User Update successfully.",
                'redirect': 'true',
                "redirect_url": reverse('admin_user:admin_user_list')
            }
    
        else:
            message = generate_form_errors(form ,formset=False)
            
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    
    else:
        
        form = AdminUserForm(instance=instance)

        context = {
            'form': form,
            'page_name' : 'Update Admin User',
            'page_title' : 'Update Admin User',
            'url' : reverse('admin_user:edit_admin_user', kwargs={'pk': pk}),
            
            'is_need_datetime_picker': True,
            'is_need_forms': True,
        }

        return render(request, 'admin_panel/pages/create/create.html',context)

@login_required
@role_required(['superadmin','admin_user'])
def delete_admin_user(request, pk):
    """
    AdminUser deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    instance = AdminUser.objects.get(pk=pk)
    current_email = instance.email
    append_email = current_email + str(randomnumber(3)) + "_deleted"
    
    instance.email = append_email
    instance.phone = randomnumber(5)
    instance.is_deleted = True
    instance.save()
    
    user = User.objects.get(username=current_email)
    user.username = append_email
    user.save()
    
    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Admin User Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('admin_user:admin_user_list'),
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')