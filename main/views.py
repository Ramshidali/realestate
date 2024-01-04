#standerd
import json
import datetime
from datetime import date, timedelta
#django
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect, HttpResponse
# third party
from rest_framework import status
#local
from main.decorators import role_required

# Create your views here.
@login_required
def app(request):
  
    return HttpResponseRedirect(reverse('main:index'))

# Create your views here.
@login_required
@role_required(['superadmin','admin_user'])
def index(request):
    today_date = timezone.now().date()
    last_month_start = (today_date - timedelta(days=today_date.day)).replace(day=1)
    
    context = {
        'page_name' : 'Dashboard',
    }
  
    return render(request,'admin_panel/index.html', context)