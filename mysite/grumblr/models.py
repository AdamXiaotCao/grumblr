from django.db import models
from django.contrib.auth.models import User
from datetime import datetime 


class Person(models.Model):
	first_name = models.CharField(max_length =30)
	last_name = models.CharField(max_length=30, default ="", blank = True)
	email_address = models.CharField(max_length=50)
	description = models.CharField(max_length = 200, default = "", blank = True)
	user = models.OneToOneField(User) 
	follows = models.ManyToManyField("self", related_name="followed+",symmetrical=False)
	blocks = models.ManyToManyField("self", related_name="blocked+",symmetrical=False)
	picture = models.ImageField(upload_to="user-photos", default = '/media/user-photos/default.jpg', blank=True)

	def __unicode__(self):
		return self.first_name + " " + self.last_name


class Comment(models.Model):
	text = models.CharField (max_length = 200,default="", blank=True)
	date = models.DateTimeField(default=datetime.now) 
	person_name = models.CharField(max_length= 30)
	person = models.ForeignKey(Person)

	def __unicode__(self):
		return self.text

class Dislike(models.Model):
	# self.managed = True
	#
	# person = models.ForeignKey(Person, null = True, blank = True)
	user_id = models.IntegerField(default= -1)
	def __unicode__(self):
		return self.id


class Grumbl(models.Model):
	text = models.CharField (max_length =200)
	person = models.ForeignKey(Person)
	date = models.DateTimeField(default=datetime.now) 
	dislikes = models.ManyToManyField(Dislike, blank=True)
	comments = models.ManyToManyField(Comment, blank=True)
	picture = models.ImageField(upload_to="grumbl-photos", blank=True)
	# dislike
	def __unicode__(self):
		return self.text


