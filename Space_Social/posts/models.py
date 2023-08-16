from typing import Iterable, Optional
from django.db import models
from django.urls import reverse
from django.conf import settings
from groups.models import Group
import mistune

from django.contrib.auth import get_user_model
User = get_user_model()

class Post(models.Model):
    group = models.ForeignKey(Group, null=True, blank=True, related_name='posts', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)

    def __str__(self) -> str:
        return self.message
    
    def save(self, *args, **kwargs):
        self.message_html = mistune.html(self.message)
        return super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('posts:single', kwargs={'username':self.user.username,
                                               'pk': self.pk})
    
    class Meta:
        ordering = ['-created_date']
        unique_together = ('user', 'message')