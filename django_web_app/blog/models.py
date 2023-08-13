from typing import Iterable, Optional
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import os



class Post(models.Model):

	TYPE_FILE = [
		('img','IMG'),
		('music','MUSIC'),
		('video','VIDEO'),
		('file','FILE'),
		('other','OTHER'),
	]

	id = models.AutoField(primary_key=True)
	title = models.CharField(max_length=100)
	file = models.FileField(null=True,blank=True,upload_to='Files')
	type_file = models.CharField(max_length=100,choices=TYPE_FILE,default='other')
	content = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	likes = models.ManyToManyField(User, related_name='blog_posts')

	def __str__(self):
		return self.title

	def extension(self):
		name, extension = os.path.splitext(self.file.name)
		return extension

	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk': self.pk})
	
	def save(self, *args, **kwargs):
		# super(Post, self).save(*args, **kwargs)
		if self.file:
			extension = self.extension()[1:]
			if extension == 'jpg' or extension == 'png' or extension == 'jpeg':
				self.type_file = 'img'
			elif extension == 'mp3' or extension == 'wav' or extension == 'ogg':
				self.type_file = 'music'
			elif extension == 'mp4' or extension == 'avi' or extension == 'mkv':
				self.type_file = 'video'
			else:
				self.type_file = 'file'
		super(Post, self).save(*args, **kwargs)


        
