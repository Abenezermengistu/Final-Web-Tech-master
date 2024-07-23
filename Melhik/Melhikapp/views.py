from admin_dashboard.views import *
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm, SendMessageForm
from django.contrib import messages
from django.db.models import Count
from django.db.models.functions import TruncDay, TruncMonth, TruncYear
from django.contrib.auth import authenticate, login as user_login, logout
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import *
import telegram
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
import requests
import random
import string


def index(request):
    reviews = Review.objects.all()
    jobs = Job.objects.all()
    freelancers = Freelancer.objects.all()
    employers = Employer.objects.all()
    seo_data = SEOSettings.objects.first()  
    context = {
      'jobs': jobs,
      'reviews': reviews,
      'freelancers': freelancers,
      'employers': employers,
      'seo_data': seo_data
    }
    return render(request, 'index.html', context)

def index_2(request):
    return render(request, 'index_2.html')

def job_search(request):
    categories = Category.objects.all()

    if request.method == 'GET':
        category_id = request.GET.get('category')
        location = request.GET.get('location')
        completed_projects = request.GET.get('completed_projects')
        pricing_type = request.GET.get('pricing_type')
        skills = request.GET.get('skills')
        availability = request.GET.get('availability')
        experience = request.GET.get('experience')
        hourly_rate_min = request.GET.get('hourly_rate_min')
        hourly_rate_max = request.GET.get('hourly_rate_max')
        keywords = request.GET.get('keywords')

        jobs = Job.objects.all()

        if category_id:
            jobs = jobs.filter(category_id=category_id)

        if location:
            jobs = jobs.filter(Q(country__icontains=location) | Q(city__icontains=location) | Q(zipcode__icontains=location))

        if completed_projects:
            jobs = jobs.filter(completed_projects=completed_projects)

        if pricing_type:
            jobs = jobs.filter(pricing_type=pricing_type)

        if skills:
            skills_list = skills.split(',')
            jobs = jobs.filter(skills__name__in=skills_list)

        if availability:
            availability_list = availability.split(',')
            jobs = jobs.filter(availability__in=availability_list)

        if experience:
            experience_list = experience.split(',')
            jobs = jobs.filter(experience__in=experience_list)

        if hourly_rate_min and hourly_rate_max:
            jobs = jobs.filter(hourly_rate__gte=hourly_rate_min, hourly_rate__lte=hourly_rate_max)

        if keywords:
            jobs = jobs.filter(Q(title__icontains=keywords) | Q(description__icontains=keywords))

        context = {
            'categories': categories,
            'jobs': jobs,
            'selected_category': category_id,
            'selected_location': location,
            'selected_completed_projects': completed_projects,
            'selected_pricing_type': pricing_type,
            'selected_skills': skills,
            'selected_availability': availability,
            'selected_experience': experience,
            'selected_hourly_rate_min': hourly_rate_min,
            'selected_hourly_rate_max': hourly_rate_max,
            'selected_keywords': keywords,
        }

        return render(request, 'job_search.html', context)

    context = {
        'categories': categories,
    }

    return render(request, 'job_search.html', context)


def onboard(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            freelancer = form.save(commit=False)
            freelancer.is_freelancer = True
            freelancer.save()
            messages.success(request, 'New freelancer registered successfully!')
        else:
            return redirect('login')
    
    else:
        form = RegistrationForm()

    return render(request, 'onboard_screen.html', {'form': form, 'messages': messages.get_messages(request)})


def onboard_screen_employer(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            employer = form.save(commit=False)
            employer.is_employer = True
            employer.save()
            messages.success(request, 'New employer registered successfully!')
                
        return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'onboard_screen_employer.html', {'emp': form, 'messages': messages.get_messages(request)})



def login_view(request):
    form = Login_Form(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email,password=password)
            if (user is not None and user.is_superuser):
                user_login(request, user)
                return redirect('admin_dashboard')
            elif user is not None and user.is_freelancer:
                user_login(request, user)
                return redirect('freelancer_dashboard')
            elif user is not None and user.is_employer:
                user_login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid Password or Email')
    return render(request, 'login.html', {'form': form})


def User_logout(request):
    logout(request)
    return redirect('index')

def error_404(request):
    return render(request, '404_page.html')

def about(request):
    return render(request, 'about.html')

def blog_grid(request):
    return render(request, 'blog_grid.html')

def cancelled_projects(request):
    return render(request, 'cancelled_projects.html')

def change_password(request):
    return render(request, 'change_password.html')

def company_details(request):
    return render(request, 'company_details.html')

def company_gallery(request, employer_id):
    employer = get_object_or_404(Employer, id=employer_id)
    context = {
        'employer': employer
    }
    return render(request, 'company_gallery.html', context)

def company_profile(request, employer_id):
    employer = get_object_or_404(Employer, id=employer_id)
    context = {
        'employer': employer
    }
    return render(request, 'company_profile.html', context)

def company_project(request, employer_id):
    employer = get_object_or_404(Employer, id=employer_id)
    context = {
        'employer': employer
    }
    return render(request, 'company_project.html', context)

def company_review(request, employer_id):
    employer = get_object_or_404(Employer, id=employer_id)
    reviews = Review.objects.all() 
    context = {
        'employer': employer,
        'reviews': reviews
    }

    return render(request, 'company_review.html', context)

def review(request):
  return render(request, 'review.html')


def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST':
        review.delete()
        return redirect('review')

@login_required
@employer_required
def dashboard(request):
    jobs = Job.objects.all()
    context = {
       'jobs': jobs
    }
    return render(request, 'dashboard.html', context)

def delete_account(request):
    return render(request, 'delete_account.html')

def deposit_funds(request):
    return render(request, 'deposit_funds.html')

def developer_list(request):
    freelancers = Freelancer.objects.all()
    total_freelancers = freelancers.count()
    context = {'freelancers': freelancers, 'total_freelancers': total_freelancers}
    return render(request, 'developer_list.html', context)

def developer_profile(request):
    return render(request, 'developer_profile.html')

def developer(request):
    return render(request, 'developer.html')

def edit_project(request):
    return render(request, 'edit_project.html')

def faq(request):
    return render(request, 'faq.html')

def favourites(request):
    return render(request, 'favourites.html')

def invited_favourites(request):
    return render(request, 'invited_favourites.html')

def favourites_list(request):
    return render(request, 'favourites_list.html')

def files(request):
    return render(request, 'files.html')


def freelancer_bookmarks(request):
    return render(request, 'freelancer_bookmarks.html')

def freelancer_cancelled_projects(request):
    return render(request, 'freelancer_cancelled_projects.html')

def freelancer_change_password(request):
  if request.method == 'POST':
    form = PasswordChangingForm(request.user, request.POST)
    if form.is_valid():  
      user = form.save()
      update_session_auth_hash(request, user)
      messages.success(request, 'Password updated!')   
      return redirect('review')
    else:
      messages.error(request, 'Please correct the error below.')
  else: 
    form = PasswordChangeForm(request.user)
  return render(request, 'freelancer_change_password.html', {'form': form})


def user_chat(request):
  chat_room = ChatRoom.objects.filter(user = request.user)
  context = {
      'users' : chat_room
  }
  return render(request, 'chats.html',context)



def messages_view(request, user_id, room_id):
    chat_room = ChatRoom.objects.filter(user = request.user)
    form = SendMessageForm(request.POST or None)
    receiver_user = CustomUser.objects.get(pk = user_id)
    room = ChatRoom.objects.get(pk = room_id)
    if request.method == 'POST':
        if form.is_valid():
            msg = form.save(commit=False)
            msg.chat =  room
            msg.sender = request.user
            msg.receiver = receiver_user
            msg.save() 


    room = ChatRoom.objects.get(id = room_id)
    message = Message.objects.filter(chat = room)
    user = CustomUser.objects.get(pk = user_id)
    context= {
        'user_message' : message,
        'user' : user,
        'form' : form,
        'users' : chat_room,
    }
    
    return render(request, 'chats.html', context)



def freelancer_completed_projects(request):
  if request.method == 'POST':
     freelancer_review = ReviewForm(request.POST)
     if freelancer_review.is_valid():
        freelancer_review.save()
        return redirect('freelancer_completed_projects')
  else:  
        freelancer_review = ReviewForm()
  return render(request, 'freelancer_completed_projects.html', {'freelancer_review': freelancer_review})

def completed_projects(request):
  if request.method == 'POST':
    form = ReviewForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('review')
  else:  
    form = ReviewForm()
  return render(request, 'completed_projects.html', {'form': form})

@login_required
@freelancer_required
def freelancer_dashboard(request):
    jobs = Job.objects.all()
    freelancer = request.user
    freelancer = Freelancer.objects.all()
    context= {
        'jobs': jobs ,
        'freelancer': freelancer
    }
    return render(request, 'freelancer_dashboard.html', context)

def freelancer_chart(request, freelancer_id):
    freelancer = Freelancer.objects.get(id=freelancer_id)

    # Get visits data grouped by day, month, and year
    visits_by_day = ProfileVisit.objects.filter(freelancer=freelancer).annotate(day=TruncDay('timestamp')).values('day').annotate(visits=Count('id'))
    visits_by_month = ProfileVisit.objects.filter(freelancer=freelancer).annotate(month=TruncMonth('timestamp')).values('month').annotate(visits=Count('id'))
    visits_by_year = ProfileVisit.objects.filter(freelancer=freelancer).annotate(year=TruncYear('timestamp')).values('year').annotate(visits=Count('id'))

    context = {
        'freelancer': freelancer,
        'visits_by_day': visits_by_day,
        'visits_by_month': visits_by_month,
        'visits_by_year': visits_by_year,
    }

    return render(request, 'freelancer_dashboard.html', context)

@login_required
def freelancer_delete_account(request):
  if request.method == 'POST':
    form = DeleteAccountForm(request.POST)
    if form.is_valid():
      if form.cleaned_data['password'] == request.user.password:
        request.user.delete()
        logout(request)
        messages.success(request, 'Your account has been deleted.')
        return redirect('home')
      else:
        messages.error(request, 'Incorrect password provided.')
  else:
    form = DeleteAccountForm()

  return render(request, 'freelancer_delete_account.html', {'form': form})

def freelancer_favourites(request):
    return render(request, 'freelancer_favourites.html')

def freelancer_files(request):
    return render(request, 'freelancer_files.html')

def freelancer_invitation(request):
    return render(request, 'freelancer_invitations.html')

def freelancer_invoices(request):
    return render(request, 'freelancer_invoices.html')

def freelancer_membership(request):
    return render(request, 'freelancer_membership.html')

def freelancer_milestones(request):
    return render(request, 'freelancer_milestones.html')

def freelancer_ongoing_projects(request):
    return render(request, 'freelancer_ongoing_projects.html')

def freelancer_payment(request):
    return render(request, 'freelancer_payment.html')

def freelancer_portfoilo(request):
    return render(request, 'freelancer_portfoilo.html')

def javascript(request):
    return render(request, 'javascript;.html')

@login_required
@freelancer_required
def freelancer_profile_settings(request):
    if request.method == 'POST':
        form = FreelancerForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            freelancer = form.save(commit=False)
            freelancer.user = request.user.freelancer
            freelancer.save()
            messages.success(request, 'You have completed your profile')
            return redirect('freelancer_profile', freelancer_id=freelancer.id)
    else:
        form = FreelancerForm(instance=request.user)

    context = {
        'form': form
    }
    return render(request, 'freelancer_profile_settings.html', context)

@login_required
def freelancer_profile(request, freelancer_id):
    freelancer = get_object_or_404(Freelancer, id=freelancer_id)

    context = {
        'freelancer': freelancer
    }

    return render(request, 'freelancer_profile.html', context)

def freelancer_review(request):
    reviews = Review.objects.all() 
    return render(request, 'freelancer_review.html',{'reviews': reviews})

def freelancer_task(request):
    return render(request, 'freelancer_task.html')

def freelancer_transaction_history(request):
    transactions = Transaction.objects.filter()

    formatted_transactions = []
    for transaction in transactions:
        paid_on = transaction.paid_on.strftime('%d %b %Y, %I:%M%p')
        formatted_transactions.append({
            'employer_name': transaction.first_name + ' ' + transaction.last_name,
            'amount': transaction.amount,
            'status': transaction.payment_method,
            'paid_on': paid_on
        })

    context = {'transactions': formatted_transactions}
    return render(request, 'freelancer_transaction_history.html', context)

def freelancer_verify_identity(request):
    return render(request, 'freelancer_verify_identity.html')

def freelancer_view_project_detail(request):
    return render(request, 'freelancer_view_project_detail.html')

import random
import string
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Transaction
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def freelancer_withdraw_money(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        payment_method = request.POST.get('payment_method')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        tx_ref = f"{first_name}-tx-{''.join(random.choices(string.ascii_lowercase + string.digits, k=10))}"

        if payment_method == 'Chapa':
            # Prepare the data for the Chapa API
            data = {
                'public_key': 'CHAPUBK_TEST-HJ7z9xGJpf4MFH6PjfpI7G45BFLCFrxf',
                'tx_ref': tx_ref,
                'amount': amount,
                'currency': 'ETB',
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'phone_number': phone_number,
                'title': 'Thank you for choosing Chapa. Your withdrawal has been processed.',
                'description': 'Paying with Confidence with Chapa.',
                'meta': {
                    'title': 'test',
                }
            }

            # Make a POST request to the Chapa API
            response = requests.post('https://api.chapa.co/v1/hosted/pay', data=data)

            # Check the response from the Chapa API (you'll need to adjust this based on the actual response format)
            if response.status_code == 200:
                Transaction.objects.create(
                    amount=amount,
                    payment_method=payment_method,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    tx_ref=tx_ref,
                )
                return HttpResponse('Withdrawal processed successfully.')
            else:
                return redirect('https://checkout.chapa.co/checkout/payment/V38JyhpTygC9QimkJrdful9oEjih0heIv53eJ1MsJS6xG')

        elif payment_method == 'Yene Pay':
            # Prepare the data for the Yene Pay API
            data = {
                "Process": "Express",
                "SuccessUrl": "https://sandbox.yenepay.com/Home/Details/73110e4c-5aec-401f-a79f-1128a023f8ed?custId=d655d940-58b4-4b81-a3dc-e80cfbf4fa75",
                "IPNUrl": "https://sandbox.yenepay.com/Home/Details/73110e4c-5aec-401f-a79f-1128a023f8ed?custId=d655d940-58b4-4b81-a3dc-e80cfbf4fa75",
                "MerchantId": "SB2564",
                "MerchantOrderId": tx_ref,  # Use the transaction reference as the order ID
                "ItemId": "1",  # Example item ID
                "ItemName": "Visitor name",  # Example item name
                "UnitPrice": amount,  # Example unit price
                "Quantity": "1",  # Example quantity
            }
            # You need to adjust the data above based on the actual requirements of the Yene Pay API

            return redirect('https://test.yenepay.com/', data)  # Redirect to the Yene Pay payment page

        else:
            return redirect('https://sandbox.yenepay.com/Home/Details/73110e4c-5aec-401f-a79f-1128a023f8ed?custId=d655d940-58b4-4b81-a3dc-e80cfbf4fa75')

    else:
        return render(request, 'freelancer_withdraw_money.html')



def logoutUser(request):
    logout(request)
    return redirect ('index')

def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                user = CustomUser.objects.get(username=username)
            except CustomUser.DoesNotExist:
                messages.error(request, 'User not found')
            else:
                # Generate a password reset token
                token_generator = default_token_generator
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = token_generator.make_token(user)

                # Build the password reset URL
                current_site = get_current_site(request)
                reset_url = f"{current_site.domain}/reset/{uid}/{token}/"

                # Send the password reset email
                subject = 'Reset Your Password'
                message = render_to_string('reset_password_email.html', {
                    'user': user,
                    'reset_url': reset_url,
                })
                send_mail(subject, message, 'from@example.com', [user.email], fail_silently=False)

                messages.success(request, 'Password reset link sent to your email')
                return redirect('login')
    else:
        form = ForgotPasswordForm()
    return render(request, 'forgot_password.html', {'form': form})


from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy

class FreelancerPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'login.html'
    form_class = SetPasswordForm

    def form_valid(self, form):
        # Call the parent form_valid method to handle password reset logic
        response = super().form_valid(form)

        # Redirect to the desired URL after resetting the password
        return redirect(reverse_lazy('login', args=[self.kwargs['freelancer_id']]))

def manage_projects(request):
    return render(request, 'manage_projects.html')

def membership_plans(request):
    return render(request, 'membership_plans.html')

def ongoing_projects(request):
    return render(request, 'ongoing_projects.html')

def pending_projects(request):
    return render(request, 'pending_projects.html')

@employer_required
@login_required
def project_form(request):
    form = JobForm()
    if request.method == 'POST':
        form = JobForm(request.POST)
        print("*********Telegram Details Mangement**********")
        print(form.errors)
        print(form.is_valid())

        if form.is_valid():
            job = form.save(commit=False)
            job.author = request.user 
            job.save()
            bot_token = '6575514030:AAFO2CwLOdy7dkZKyMosGNmZuVMPXHL0ZlQ'
            chat_id = '-1001913256564'
            text = (
                f"New Job Alert: {job.project_title}\n"
                f"Category: {job.category_type}\n" 
                f"Price: {job.price}Birr\n"
                f"Duration: {job.duration}\n"
                f"Start Date: {job.start_date}\n" 
                f"Reference Links: {job.reference_links}\n"
                f"Description: {job.project_description}"
            )
         
            url = f'https://api.telegram.org/bot{bot_token}/sendMessage'

            data = {
                'chat_id': chat_id,
                'text': text
            }
            
            response = requests.post(url, data=data)

            if response.status_code == 200:
                print('Message sent!')
            else:
                print('Error sending message:')
                print(response.text)
            messages.success(request, 'New Job Posted successfully!')
        
    context = {
        'form': form,
        'categories': Category.objects.all(),
    }
    return render(request, 'post_project.html', context)

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

@employer_required
def profile_settings(request):
    if request.method == 'POST':
        form = EmployerForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            employer = form.save(commit=False)
            employer.user = request.user
            employer.save()
            messages.success(request, 'Profile Posted successfully!')
            # return redirect('company_profile', employer_id=employer.id)
    else:
        form = EmployerForm(instance=request.user)
    context = {
        'form': form
    }
    return render(request, 'profile_settings.html', context)

def user_account_details(request):
  freelancer_profile = Freelancer.objects.get(user=request.user)
  context = {
    'profile': freelancer_profile
  }
  return render(request, 'user-account-details.html', context)


def project_payment(request):
    return render(request, 'project_payment.html')

@login_required
def project_details(request, project_id):
    project = Job.objects.get(id=project_id)
    proposals = ProjectProposal.objects.filter(job=project)
    freelancer = Freelancer.objects.all()
    
    if request.method == 'POST':
        form = ProposalForm(request.POST)
        if form.is_valid():
            price = form.cleaned_data['price']
            hours = form.cleaned_data['hours']
            cover_letter = form.cleaned_data['cover_letter']
            
            # Save the proposal to the database
            proposal = ProjectProposal(
                job=project,  # Assign the associated Job instance
                price=price,
                hours=hours,
                cover_letter=cover_letter,
                freelancer=request.user  # Assign the logged-in user directly
            )
            proposal.save()
            
            # Refresh the proposals queryset with the updated data
            proposals = ProjectProposal.objects.filter(job=project)
            
            # Add success message
            messages.success(request, 'Proposal has been sent. The client will contact you soon.')
            
            # Redirect to the same page to prevent form resubmission
            return redirect('project_details', project_id=project_id)
    else:
        form = ProposalForm()
    
    return render(request, 'project_details.html', {'project': project, 'proposals': proposals, 'form': form, 'freelancer': freelancer})

def create_check_room(request, pk):
    user_one = request.user
    user_two = CustomUser.objects.get(pk=pk)
    common_room = ChatRoom.objects.filter(user = user_one).filter(user=user_two)
    if common_room.exists():
        return redirect(messages_view, user_id=user_one.id, room_id = common_room.first().id)
    else:
        obj = ChatRoom()
        obj.save()

        obj.user.set(user_one,user_two)
        return redirect(messages_view, user_id=user_one.id, room_id = common_room.first().id)
    

@employer_required
def project_proposals(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    proposals = ProjectProposal.objects.filter(job=job)
    freelancer = Freelancer.objects.filter(user=request.user)
    proposal_count = proposals.count()

    return render(request, 'project_proposals.html', {'job': job, 'proposals': proposals, 'proposal_count': proposal_count, 'freelancer': freelancer})

def freelancer_project_proposals(request):
    return render(request, 'freelancer_project_proposals.html')

def project(request):
    jobs = Job.objects.all()
    num_projects = Job.objects.count()
    project_title = request.GET.get('project_title')
    if project_title:
      jobs = jobs.filter(project_title__icontains=project_title)
    print("Filter by: ", request.GET.get('project_title'))
    total_projects = Job.objects.all().count()
    return render(request, 'project.html', {'jobs': jobs, 'num_projects': num_projects, 'total_projects': total_projects})


def tasks(request):
    return render(request, 'tasks.html')

def term_condition(request):
    return render(request, 'term_condition.html')


def verify_identity(request):
    return render(request, 'verify_identity.html')

def video_call(request):
    return render(request, 'video_call.html')

def view_invoice(request):
    return render(request, 'view_invoice.html')

def view_project_detail(request):
    return render(request, 'view_project_detail.html')

def voice_call(request):
    return render(request, 'voice_call.html')

def invoices(request):
    return render(request, 'invoices.html')


from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler, CommandHandler, Updater, MessageHandler, Filters

def telegram_conversation(request):
    # Define the conversation states
    FREELANCER, EMPLOYER = range(2)
    USERNAME, FIRST_NAME, LAST_NAME, EMAIL, PASSWORD = range(5)

    def start(update, context):
        reply_keyboard = [['Freelancer', 'Employer']]
        update.message.reply_text(
            'Please select whether you are a Freelancer or Employer:',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        )
        return FREELANCER

    def freelancer_employer(update, context):
        user = update.message.text
        context.user_data['user'] = user
        update.message.reply_text('Please enter your credentials:', reply_markup=ReplyKeyboardRemove())
        return USERNAME

    def username(update, context):
        username = update.message.text
        if not username:
            update.message.reply_text("Please enter a username")
            return USERNAME
        context.user_data['username'] = username
        return FIRST_NAME

    def first_name(update, context):
        first_name = update.message.text
        if not first_name:
            update.message.reply_text("Please enter your first name")
            return FIRST_NAME
        context.user_data['first_name'] = first_name
        return LAST_NAME

    def last_name(update, context):
        last_name = update.message.text
        if not last_name:
            update.message.reply_text('Please enter your last name')
            return LAST_NAME
        context.user_data['last_name'] = last_name
        return EMAIL

    def email(update, context):
        email = update.message.text
        if not email:
            update.message.reply_text("Please enter your email")
            return EMAIL
        context.user_data['email'] = email
        return PASSWORD

    def password(update, context):
        password = update.message.text
        if not password:
            update.message.reply_text("Please enter a password")
            return PASSWORD
        if len(password) < 8:
            update.message.reply_text("Password must be at least 8 characters")
            return PASSWORD
        if not any(char.isalpha() for char in password) or not any(char.isdigit() for char in password):
            update.message.reply_text("Password must contain letters and numbers")
            return PASSWORD
        context.user_data['password'] = password
        return "done"

    def done(update, context):
        # Create a new user using the collected data
        user_data = context.user_data
        form = RegistrationForm(user_data)
        if form.is_valid():
            form.save()
            update.message.reply_text("Thank you for choosing KofeJob")
            return ConversationHandler.END
        else:
            error_messages = form.errors.get_json_data()
            error_text = "\n".join([f"{field}: {', '.join(errors)}" for field, errors in error_messages.items()])
            update.message.reply_text(f"Input validation failed:\n{error_text}")
            return ConversationHandler.END

    def fallback(update, context):
        update.message.reply_text("Invalid input")
        return ConversationHandler.END

    # Create the ConversationHandler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FREELANCER: [MessageHandler(Filters.text, freelancer_employer)],
            USERNAME: [MessageHandler(Filters.text, username)],
            FIRST_NAME: [MessageHandler(Filters.text, first_name)],
            LAST_NAME: [MessageHandler(Filters.text, last_name)],
            EMAIL: [MessageHandler(Filters.text, email)],
            PASSWORD: [MessageHandler(Filters.text, password)],
        },
        fallbacks=[MessageHandler(Filters.regex("^Done$"), done)]
    )

    # Create an updater and add the conversation handler
    TELEGRAM_TOKEN = '6575514030:AAFO2CwLOdy7dkZKyMosGNmZuVMPXHL0ZlQ'
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    updater.dispatcher.add_handler(conv_handler)

    # Start the conversation
    updater.start_polling()

    # Return a response to indicate that the conversation has started
    return HttpResponse("Telegram conversation started.")