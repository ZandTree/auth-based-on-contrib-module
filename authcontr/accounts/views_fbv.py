from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse_lazy
from django.views import generic
from .models import Profile
from django.contrib.auth.views import LoginView,LogoutView # singup don't exist make your own
from django.contrib.auth import logout # to use with redirect view
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserCreateForm,LogoutForm
from django.contrib import messages
# new for fbv signup with email confirmation
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.models import User

class  ProfileView(LoginRequiredMixin,generic.DetailView):
    template_name = 'accounts/profile.html'
    model = Profile
    context_object_name = 'profile'

    def get_object(self,queryset=None):
        obj = get_object_or_404 (
            Profile,
            user = self.request.user
        )
        if obj.user != self.request.user:
            raise Http404
        return obj

# seems not safe emough == with .get() method
# class LogoutView(generic.RedirectView):
#     #template_name = 'registration/logout.html'
#     url = reverse_lazy('home')
#     def get(self,request,*args,**kwargs):
#         logout(request)
#         return super().get(request,*args,**kwargs)

# logout through post method ==> seems safer
class LogoutView(LoginRequiredMixin,generic.FormView):
    form_class = LogoutForm # see forms.py simple form just for post request
    template_name = 'accounts/logout.html'

    def form_valid(self,form):
        logout(self.request)
        return redirect('home')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
#cbv without email confirmation
# class SignUpView(generic.CreateView):
#     form_class = UserCreateForm
#     template_name = 'accounts/signup.html'
#     success_url = reverse_lazy('accounts:login')
#

def signup(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = UserCreateForm()
    return render(request, 'accounts/signup.html', {'form': form})







# class MyPasswordChangeView(PasswordChangeView):
    #docs built-in success_url = reverse_lazy('password_change_done')
    success_url = reverse_lazy('accounts:profile_view')
    def form_valid(self,form):
        messages.success(self.request,'Password has been updated!')
        return super().form_valid(form)
