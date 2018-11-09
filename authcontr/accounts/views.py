from django.shortcuts import render,get_object_or_404
from django.views import generic
from .models import Profile

class ProfileView(generic.DetailView):
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
