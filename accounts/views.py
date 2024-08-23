from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.views import PasswordChangeView, LogoutView, PasswordResetView, LoginView
from .forms import CustomAuthenticationForm


from .forms import CustomUserCreationForm, CustomProfileChangeForm
from .models import CustomUser, Profile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout

from .models import Profile
from django.http import HttpResponse
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    def get_success_url(self):
        return '/'

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('accounts:login')
        else:
            return render(request, self.template_name, {'form' : form })
    def form_valid(self, form):
            user_instance = form.instance
            if CustomUser.objects.filter(username=user_instance.username).exists():
                response = super().form_valid(form)
                Profile.objects.create(user=user_instance)
                return response
            else:
                return HttpResponse("User does not exist", status=404)
            
        
        

        
class ProfilePageView(LoginRequiredMixin,DetailView):
    model = Profile
    template_name = 'profile.html'
    context_object_name = 'profile'

class ProfileUpdateView(LoginRequiredMixin,UpdateView):
    model = Profile
    form_class = CustomProfileChangeForm
    template_name = 'profile_edit.html'
    class Meta:
        labels = {
            'fname': 'First Name',
            'lname': 'Last Name',
            'biography': 'Biography',
            'picture': 'Profile Picture',
        }
        crispy_field_class = 'bg-info'

    def get_success_url(self):
        return reverse_lazy('accounts:profile_view', args=[str(self.request.user.profile.id)])

        
        
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'registration/password_change_form.html'
    success_url = reverse_lazy('accounts:password_change_done')


    def form_valid(self, form):
        user = form.save(commit=False)
        token_generator = default_token_generator
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)
        
        reset_url = reverse_lazy('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
        reset_url = self.request.build_absolute_uri(reset_url)
        
        # Render the email template with the password reset URL
        email_context = {'reset_url': reset_url}
        email_html_message = render_to_string(self.email_template_name, email_context)
        
        # Send the email
        send_mail(
            subject='Password Reset',
            message='',
            html_message=email_html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        
        return super().form_valid(form)
    
    
        
class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_Form.html'
    success_url = reverse_lazy('accounts:password_reset_done')

class CustomLoginView(LoginView):
    template_name = 'registration/login.html' 
    authentication_form = CustomAuthenticationForm  
    

class CustomLogoutView(LogoutView):
    template_name = 'registration/logout.html'
    next_page = reverse_lazy('accounts:login')  
    
def logout_view(request):
    logout(request) 
    return redirect('accounts:login')