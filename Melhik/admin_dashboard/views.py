from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login as admin_login
from Melhikapp.forms import *
from Melhikapp.models import *
from django.http import HttpResponse
from Melhikapp.decorators import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import datetime
from django.db.models import Count
import time
from django.db.models.functions import TruncDay



def admin_index(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_superuser:
                # Fix: login() takes the request and user 
                admin_login(request, user) 
                # messages.success(request, 'You are now logged in')
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'Only superadmin can log in')
                return render(request, 'admin.html', {'error': 'Only superadmin can log in'})
        else:
                messages.error(request, 'Invalid login')
                return render(request, 'admin.html', {'error': 'Invalid login'})

    return render (request , 'admin.html')

def admin_logout(request):
    logout(request)
    return redirect('index')

@login_required
@admin_user_required
def admin_dashboard(request):
    total_num_users = CustomUser.objects.count()
    total_jobs = Job.objects.count()
    reviews = Review.objects.all()

    return render(request, 'admin_dashboard.html', {
        'reviews': reviews,
        'total_num_users': total_num_users,
        'total_jobs': total_jobs,
    })


from django.db.models import Count
from django.http import JsonResponse

def get_jobs_count(request):
    jobs_count = (
        Job.objects
        .values('timestamp__month')
        .annotate(count=Count('id'))
        .order_by('timestamp__month')
    )
    
    month_categories = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    month_colors = [
        '#FF0000',  # Jan
        '#00FF00',  # Feb
        '#0000FF',  # Mar
        '#FF00FF',  # Apr
        '#FFFF00',  # May
        '#00FFFF',  # Jun
        '#FF8000',  # Jul
        '#8000FF',  # Aug
        '#008000',  # Sep
        '#800000',  # Oct
        '#000080',  # Nov
        '#808080',  # Dec
    ]
    
    data = {
        'categories': month_categories,
        'series': [{
            'name': 'Count',
            'data': [0] * 12,  # Initialize all counts as 0
            'colors': month_colors  # Assign the colors for each column
        }]
    }
    
    for item in jobs_count:
        month = item['timestamp__month']
        count = item['count']
        data['series'][0]['data'][month-1] = count
    
    return JsonResponse(data)




def get_users_count(request):
    user_count = CustomUser.objects.count()
    job_count = Job.objects.count()

    data = {
        'series': [
            {
                'name': 'Users',
                'y': user_count
            },
            {
                'name': 'Jobs',
                'y': job_count
            }
        ]
    }

    return JsonResponse(data)


@login_required
@admin_user_required
def get_user_growth(request):
    user_data = CustomUser.objects.annotate(date=TruncDay('date_joined')).values('date').annotate(total=Count('id')).order_by('date')

    dates = [entry['date'].strftime('%Y-%m-%d') for entry in user_data]
    totals = [entry['total'] for entry in user_data]

    data = {
        'dates': dates,
        'series': [{
            'name': 'Total Users',
            'data': totals
        }]
    }

    return JsonResponse(data)




def activities(request):
    return render(request, 'activities.html')

def categories(request):
    if request.method == 'POST':
        name = request.POST.get('category_name')
        category = Category(name=name)
        category.save()
        return redirect('categories')

    categories = Category.objects.all()
    return render(request, 'categories.html', {'categories': categories})

def delete_category(request, category_id):
     category = Category.objects.get(id=category_id)
     category.delete()
     return redirect('categories')

def data_tables(request):
    return render(request, 'data_tables.html')

def deposit(request):
    return render(request, 'deposit.html')

def deposit_cancelled(request):
    return render(request, 'deposit_cancelled.html')

def deposit_completed(request):
    return render(request, 'deposit_completed.html')

def deposit_hold(request):
    return render(request, 'deposit_hold.html')

def deposit_pending(request):
    return render(request, 'deposit_pending.html')

def earning_employer(request):
    return render(request, 'earning_employer.html')

def earning_freelancer(request):
    return render(request, 'earning_freelancer.html')

def email_settings(request):
    return render(request, 'email_settings.html')

def employe_list(request):
    return render(request, 'employe_list.html')

def forget_password(request):
    return render(request, 'forget_password.html')

def freelance_list(request):
    return render(request, 'freelance_list.html')

def localization_details(request):
    return render(request, 'localization_details.html')

def login(request):
    return render(request, 'login.html')

def other_settings(request):
    return render(request, 'other_settings.html')

def payment_settings(request):
    return render(request, 'payment_settings.html')

def projects(request):
    jobs = Job.objects.select_related('author').all()
    total_jobs = Job.objects.count()
    context = {
        'jobs': jobs,
        'total_jobs': total_jobs
    }
    return render(request, 'projects.html', context)

def project_bidding(request):
    return render(request, 'project_bidding.html')

def project_earnings(request):
    return render(request, 'project_earnings.html')

def project_invoice(request):
    return render(request, 'project_invoice.html')

def users(request):
    freelancers = Freelancer.objects.all()

    context = {
        'freelancers': freelancers,
    }

    return render(request, 'users.html', context)

def withdrawn(request):
    return render(request, 'withdrawn.html')

def withdrawn_pending(request):
    return render(request, 'withdrawn_pending.html')

def withdrawn_cancelled(request):
    return render(request, 'withdrawn_cancelled.html')

def withdrawn_completed(request):
    return render(request, 'withdrawn_completed.html')

def transaction(request):
    return render(request, 'transaction.html')

def transaction_onhold(request):
    return render(request, 'transaction_onhold.html')

def transaction_pending(request):
    return render(request, 'transaction_pending.html')

def transaction_withdraw(request):
    return render(request, 'transaction_withdraw.html')

def transaction_deposit(request):
    return render(request, 'transaction_deposit.html')

def transaction_completed(request):
    return render(request, 'transaction_completed.html')

def providers(request):
    return render(request, 'providers.html')

def subscription(request):
    return render(request, 'subscription.html')

def subscripe_freelancer(request):
    return render(request, 'subscripe_freelancer.html')

def reports(request):
    return render(request, 'reports.html')

def roles(request):
    return render(request, 'roles.html')

def roles_permission(request):
    return render(request, 'roles_permission.html')

def skills(request):
    return render(request, 'skills.html')

def verify_identity(request):
    return render(request, 'verify_identity.html')

def admin_settings(request):
    return render(request, 'settings.html')


def users(request):
    # Get the freelancers
    freelancers = CustomUser.objects.filter(is_freelancer=True)

    # Update the status of each freelancer to active
    for freelancer in freelancers:
        freelancer.status = 'active'
        freelancer.save()

    # Render the users.html template with the freelancers
    return render(request, 'users.html', {'freelancers': freelancers})

def user_suspended(request):
    # Get the freelancers
    freelancers = CustomUser.objects.filter(is_freelancer=True)

    # Update the status of each freelancer to suspended
    for freelancer in freelancers:
        freelancer.status = 'suspended'
        freelancer.save()

    # Render the user_suspended.html template
    return render(request, 'user_suspended.html')


def social_links(request):
    return render(request, 'social_links.html')

def others_settings(request):
    return render(request, 'others_settings.html')

def seo_settings(request):
    seo_settings_obj = SEOSettings.objects.first()
    
    if request.method == 'POST':
        form = SEOSettingsForm(request.POST, instance=seo_settings_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Home Page Details Was Been Updated')
    else:
        form = SEOSettingsForm(instance=seo_settings_obj)
    
    return render(request, 'seo_settings.html', {'form': form})
        
def user_suspended(request):
    return render(request, 'user_suspended.html')

def social_settings(request):
    return render(request, 'social_settings.html')