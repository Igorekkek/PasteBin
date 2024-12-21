from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Post(models.Model):
    content = models.TextField(blank=True, verbose_name="Текст сниппета")
    password = models.CharField(blank=True, max_length=200, verbose_name='Пароль')
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Пользователь", null=True, blank=True)

    def __str__(self):
        return self.content[:15]
    
    def get_absolute_url(self):
        return {'view' : reverse('viewpost', kwargs={'post_id' : self.id}),
                'delete' : reverse('deletepost', kwargs={'post_id' : self.id}),
                'change' : reverse('changepost', kwargs={'post_id' : self.id})
        }
    
    def get_index_url(self):
        return self.get_absolute_url()