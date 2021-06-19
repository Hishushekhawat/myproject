from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	date_created = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	likes = models.ManyToManyField(User, related_name='likes',blank=True)

	def __str__(self):
		return self.title

	def total_likes(self):
		return self.likes.count()

	def get_absolute_url(self):
		return reverse('post-detail',kwargs={'pk':self.pk})

class Comment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	content = models.CharField(max_length=150)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return '{}-{}'.format(self.post.title, str(self.user.username))

	def total_comment(self):
		return self.comment.count()

	def get_absolute_url(self):
		return reverse('post-detail',kwargs={'pk':self.pk})
