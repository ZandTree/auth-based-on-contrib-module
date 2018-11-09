from django.db import models
from django.contrib.auth.models import User
from django.contrib import messages
from PIL import Image
from django.dispatch import receiver
from django.utils import timezone
from django.db.models.signals import post_save
import os

def get_ava_image(instance,file):
    file_name = file.split('.')
    start = file_name[0]
    extention = file_name[-1]
    time = timezone.now().strftime('%Y-%m-%d')
    if len(start) > 10:
        start = start[:10]
    generic_name = time + '_'+ start + '.' + end
    return os.path.join('ava_image','user_{0}','{1}').format(instance.user_id,generic_name)

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    first = models.CharField(max_length=30,blank=True)
    last_name = models.CharField(max_length=50,blank=True)
    birth = models.DateField(blank=True)
    bio = models.TextField(default="",max_length=300)
    location = models.CharField(max_length=30,blank=True)
    ava = models.ImageField(blank=True,null=True,upload_to=get_ava_image)

    def save(self,**kwargs):
        super().save(**kwargs)
        if self.ava:
            image = Image.open(self.ava.path)
            if image.height > 250 or image.width > 250:
                output_size = (250,250)
                img.thumbnail(output_size)
                img.save(self.avatar.path)
    @property
    def get_name(self):
        if self.first and self.last:
            return "{} {}".format(self.first,self.last_name)
        elif self.first:
            return self.first
        else:
            return self.user.username
    @property
    def get_ava_name(self):
        if self.ava:
            return '/media/{}'.format(self.ava)
        else:
            return '/static/img/default_ava.png/'

@receiver(post_save,sender=User)
def create_user(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user = instance)

@receiver(post_save,sender=User)
def save_user_profile(sender,instance,**kwargs):
    instance.profile.save()
