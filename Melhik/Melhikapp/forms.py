from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from django_countries import Countries 
from django_countries.fields import CountryField


class SendMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content',]


class CategoryForm(forms.Form):
    pass
    name = forms.CharField(label='Category Name', max_length=100)


class AccountTypeForm(forms.Form):
    account_type = forms.ChoiceField(choices=(
        ('freelancer', 'Freelancer'),
        ('employer', 'Employer')
    ))

# RegistrationForm
class RegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=25, required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField()
    password1 = forms.CharField(max_length=40, label='Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Your Password',
        'autocomplete': 'off',
        'value': '*******'
    }))
    password2 = forms.CharField(max_length=40, label='Confirm Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm Password',
        'autocomplete': 'on',
        'value': '*******'
    }))

    photo = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Add Photo(Optional)',
   
    }))
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter User Name'})
        self.fields['first_name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter First Name'})
        self.fields['last_name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter Last Name'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter Email'})

    class Meta:
        model = CustomUser
        fields = 'username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'photo'

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            self.add_error('password2', "Passwords do not match")


# FreelancerForm

gender_list = [
    ('male', 'Male'),
    ('female', 'Female'),
]

language_choices = (
    ('English', 'English'),
    ('Spanish', 'Spanish'),
    ('French', 'French'),
    ('Russian', 'Russian'),
    ('German', 'German')
)

class FreelancerForm(forms.ModelForm):
    email = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    hourly_rate = forms.CharField(validators=[RegexValidator(r'^\d+$', 'Hourly rate must be a number')],widget=forms.TextInput(attrs={'class': 'form-control' }))
    gender = forms.ChoiceField(choices=gender_list, widget=forms.Select(attrs={'class': 'form-control select'}))
    country = CountryField(blank_label='(select country)')
    contact_number = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control datepicker', 'type': 'date'}))
    language = forms.ChoiceField(choices=language_choices, widget=forms.Select(attrs={'class': 'form-control select'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    zipcode = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    overview = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control summernote', 'rows': '5'}))
    experience_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    experience_company = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    experience_start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control datepicker', 'type': 'date'}))
    experience_end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control datepicker', 'type': 'date'}))
    experience_summary = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control summernote', 'rows': '5'}))
    degree = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    institution = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    start_year = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control datepicker', 'type': 'date'}))
    end_year = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control datepicker', 'type': 'date'}))
    education_summary = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control summernote', 'rows': '5'}))
    linked_in = forms.URLField(max_length=200, required=False, label="LinkedIn:", widget=forms.URLInput(attrs={'class': 'form-control'}))
    git_hub = forms.URLField(max_length=200, required=False, label="Github:", widget=forms.URLInput(attrs={'class': 'form-control'}))
    profile_picture = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    banner_image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

    class Meta: 
        model = Freelancer
        exclude = ['user']
        fields = '__all__'
        

    def clean_profile_picture(self):
      profile_picture = self.cleaned_data['profile_picture']
      file_size = profile_picture.size

      limit_kb = 1024
      if file_size > limit_kb * 1024:
          raise ValidationError("Max size is 1MB")
      return profile_picture

    def clean_banner_image(self):
      banner_image = self.cleaned_data['banner_image']
      file_size = banner_image.size

      limit_kb = 1024
      if file_size > limit_kb * 1024:
          raise ValidationError("Max size is 1MB")
      return banner_image
    
    def clean_country(self):

       location = self.cleaned_data['location']
       
       if location:
         return location.country
       else:
        return ""
    

class EmployerForm(forms.ModelForm):
    team_size_min = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Minimum Team Size'})
    )
    team_size_max = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Maximum Team Size'})
    )

    class Meta:
        model = Employer
        fields = ['company_name', 'owner_name', 'team_size_min', 'team_size_max', 'company_logo', 'overview', 'established_date', 'phone_number', 'website', 'country', 'address_line_2', 'city']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'}),
            'owner_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Owner Name'}),
            'company_logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'overview': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Overview'}),
            'established_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Established Date', 'type': 'date'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Website'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'address_line_2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Address Line 2"}),
            "city": forms.TextInput(attrs={"class": "form-control", "placeholder": "City"})
        }

class Login_Form(forms.Form):
    email = forms.EmailField(
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter email',
                'class': 'form-control'
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control floating',
            'placeholder': 'Enter Password',
            'required': 'true',
            'value': '*******'
        })
    )
    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       print(self.fields['email'].validators)

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = '__all__'
        exclude = ['author', 'timestamp']
        widgets = {
            'project_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Project title'}),
            'category_type': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'duration': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'documents': forms.FileInput(attrs={'class': 'form-control'}),
            'reference_links': forms.TextInput(attrs={'class': 'form-control'}),
            'project_description': forms.Textarea(attrs={'class': 'form-control summernote', 'rows': '5'}),
        }

class ForgotPasswordForm(forms.Form):
    username = forms.CharField(
        max_length=25,
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter username',
                'class': 'form-control'
            }
        )
    )

class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Old Password'}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm new password'}))
    class Meta:
        model = CustomUser
        fields = ['old_password', 'new_password', 'confirm_password']
        
class DeleteAccountForm(forms.Form):
  password = forms.CharField(widget=forms.PasswordInput)

class StarRatingWidget(forms.Widget):

    def render(self, name, value, attrs=None, renderer=None):
        stars = """
    <style>
        .rating {
          display: flex;
        }

        input[type="radio"] { 
          display: none;
        }

        label {
          cursor: pointer;
        }

        label:before {
          content: "★";
          margin-right: 5px;
          color: #ddd;
          font-size: 30px;
        }

        input[type="radio"]:checked ~ label:before {
          color: gold; 
        }
      </style>
    <div class="rating">
      <input 
        type="radio" 
        id="star5" 
        name="rating" 
        value="5"
      /><label for="star5"></label>

      <input 
        type="radio" 
        id="star4" 
        name="rating" 
        value="4"  
      /><label for="star4"></label>

      <input 
        type="radio" 
        id="star3" 
        name="rating" 
        value="3"
      /><label for="star3"></label>

      <input 
        type="radio" 
        id="star2" 
        name="rating" 
        value="2"
      /><label for="star2"></label> 

      <input
        type="radio" 
        id="star1"
        name="rating"
        value="1" 
      /><label for="star1"> </label>
    </div>
    """
        if value:
            stars = stars.replace('value="★"' % value, 'checked')

        return stars


class ReviewForm(forms.ModelForm):

    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Write Your Review'
                }
        )
    )

    rating = forms.IntegerField(
        widget=StarRatingWidget,
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['rating'].widget.value = self.instance.rating

    class Meta:
        model = Review
        fields = ['message', 'rating']


class ProposalForm(forms.Form):
    price = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Price'}))
    hours = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Estimated Hours'}))
    cover_letter = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '5', 'placeholder': 'Cover Letter'}))
    agree_terms = forms.BooleanField(required=True)


class TelegramRegistrationForm(RegistrationForm):
    telegram_chat_id = forms.CharField(max_length=255, required=True)

    class Meta(RegistrationForm.Meta):
        model = CustomUser

    def save(self, commit=True):
        user = super().save(commit=False)
        user.telegram_chat_id = self.cleaned_data['telegram_chat_id']
        if commit:
            user.save()
        return user
    


class SEOSettingsForm(forms.ModelForm):
    class Meta:
        model = SEOSettings
        fields = ('meta_title', 'meta_keywords', 'meta_description')