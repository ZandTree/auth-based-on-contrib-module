from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse_lazy
from django.views import generic
from .models import Profile
from django.contrib.auth.views import LoginView,LogoutView # singup don't exist make your own
from django.contrib.auth import logout # to use with redirect view
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserCreateForm,LogoutForm

class ProfileView(LoginRequiredMixin,generic.DetailView):
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

class SignUpView(generic.CreateView):
    form_class = UserCreateForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:login')
