from django.db import models
from time import time
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.
def image_folder(instance, filename):
	filename = instance.slug+'.'+filename.split('.')[1]
	return '{}/{}'.format(instance.slug, filename)

def gen_slug(name):
	slug = slugify(name, allow_unicode=True)
	return slug+'-'+str(int(time()))

class Action(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	name = models.CharField(max_length=150)
	slug = models.SlugField(max_length=150, unique=True, blank=True)
	time_to_do_hour = models.IntegerField(blank=True)
	time_to_do_minute = models.IntegerField(blank=True)
	time_should_be_hour = models.IntegerField(blank=True)
	time_should_be_minute = models.IntegerField(blank=True)
	data = models.DateTimeField(auto_now_add=True)
	description = models.TextField(max_length=250, blank=True)
	category = models.ManyToManyField('Category', blank=True, related_name='actions')
	time_trigger = models.BooleanField(default=False)
	is_available = models.BooleanField(default=True)

	def save(self, *args, **kwargs):
		self.slug=gen_slug((self.name))
		super().save(*args, **kwargs)

	def get_hidden_url(self):
		return reverse('hidden_url', kwargs={'slug':self.slug})

	def get_delete_url(self):
		return reverse('delete_url', kwargs={'slug':self.slug})	

	def get_restore_url(self):
		return reverse('restore_url', kwargs={'slug':self.slug})	

	def get_update_url(self):
		return reverse('update_url', kwargs={'slug':self.slug})


	def __str__(self):
		return self.name + '-'+str(self.data.year)+'-'+str(self.data.month)+'-'+str(self.data.day)+' Time:'+str(self.data.hour)+':'+str(self.data.minute)

class Category(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
	name = models.CharField(max_length=100)
	slug= models.SlugField(max_length=170, blank=True)
	total_time = models.IntegerField(default=0)

	def save(self, *args, **kwargs):
		self.slug = gen_slug('category-'+self.name)
		super().save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('category_url', kwargs={'slug':self.slug})	

	def get_delete_url(self):
		return reverse('delete_url', kwargs={'slug':self.slug})


	def __str__(self):
		return self.name