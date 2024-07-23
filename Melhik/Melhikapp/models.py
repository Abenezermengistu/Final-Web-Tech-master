from django.db import models
from django.conf import settings
from admin_dashboard.models import *
from django_countries.fields import CountryField
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
  is_freelancer = models.BooleanField(default=False)
  is_employer = models.BooleanField(default=False)
  email = models.EmailField(unique=True)
  photo = models.ImageField(upload_to='UserPhoto', null=True, blank=True)
  telegram_chat_id = models.CharField(max_length=255, null=True, blank=True)

  EMAIL_FIELD = 'email'
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['username', 'first_name', 'last_name']


gender_list = [
    ('M', 'Male'),
    ('F', 'Female'),
]

language_choices = [
  ('English', 'English'),
  ('Spanish', 'Spanish'), 
  ('French', 'French'),
  ('Russian', 'Russian'),
  ('German', 'German'),
]

class Freelancer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.SET_NULL, null=True)
    email = models.EmailField(max_length=100)
    hourly_rate = models.CharField(max_length=10, help_text='ETB', validators=[RegexValidator(r'^\d+$', 'Hourly rate must be a number')])
    contact_number = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=gender_list)
    language = models.CharField(max_length=100, choices=language_choices)
    profile_picture = models.ImageField(upload_to='freelancer_profiles')
    banner_image = models.ImageField(upload_to='freelancer_banners')
    address = models.TextField()
    country = CountryField()
    zipcode = models.CharField(max_length=100)
    overview = models.TextField()
    experience_name = models.CharField(max_length=100)
    experience_company = models.CharField(max_length=100)  
    experience_start_date = models.DateField()
    experience_end_date = models.DateField()
    experience_summary = models.TextField()
    degree = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    start_year = models.DateField()  
    end_year = models.DateField()
    education_summary = models.TextField()
    linked_in = models.URLField(blank=True, null=True)
    git_hub = models.URLField(blank=True, null=True)


    def __str__(self):
        return self.email
    
class Employer(models.Model):
  user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
  company_name = models.CharField(max_length=100) 
  owner_name = models.CharField(max_length=100)
  team_size_min = models.IntegerField()
  team_size_max = models.IntegerField()
  company_logo = models.FileField()
  overview = models.TextField()
  established_date = models.DateField()
  phone_number = models.CharField(max_length=20)
  website = models.CharField(max_length=100)
  country = models.CharField(max_length=100)
  address_line_2 = models.CharField(max_length=100) 
  city = models.CharField(max_length=100)
  timestamp = models.DateTimeField(auto_now_add=True)

  def __str__(self):
     return self.company_name

  def get_team_size_range(self):
    return f"{self.team_size_min}-{self.team_size_max}"

    
class Job(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    project_title = models.CharField(max_length=100)
    category_type = models.CharField(max_length=100)
    price = models.IntegerField()
    duration = models.CharField(max_length=100, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    documents = models.FileField(upload_to='documents/', null=True, blank=True)
    reference_links = models.CharField(max_length=255, null=True, blank=True)
    project_description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.project_title
    
    def save(self, *args, **kwargs):
        if not self.id and self.author is None:
            raise ValueError("Author must be set before saving the job.")
        super().save(*args, **kwargs)

class Review(models.Model):
  message = models.TextField()
  rating = models.IntegerField()
  timestamp = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.message


class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    publication_date = models.DateField()

class Transaction(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=200)
    email = models.EmailField()
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    tx_ref = models.CharField(max_length=200)

class ProfileVisit(models.Model):
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class ChatRoom(models.Model):
  user = models.ManyToManyField(CustomUser, related_name='chats')

class Message(models.Model):
  chat = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
  sender = models.ForeignKey(CustomUser, related_name='sent_messages', on_delete=models.CASCADE) 
  receiver = models.ForeignKey(CustomUser, related_name='received_messages', on_delete=models.CASCADE)
  content = models.TextField()
  timestamp = models.DateTimeField(auto_now_add=True)


class ProjectProposal(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    freelancer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    hours = models.PositiveIntegerField()
    cover_letter = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Proposal for Job: {self.job} by Freelancer: {self.freelancer}"

class SEOSettings(models.Model):
    meta_title = models.CharField(max_length=255)
    meta_keywords = models.CharField(max_length=255)
    meta_description = models.TextField()