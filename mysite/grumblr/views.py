from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.db import transaction


import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.tokens import default_token_generator

from django.core.mail import send_mail
from mimetypes import guess_type
from grumblr.models import *
from grumblr.forms import *

# Create your views here.
@login_required
def search(request):
	if 'target' in request.GET:
		content = request.GET['target']
		allgrumbls = Grumbl.objects.filter(text__contains=content)
		context = {'allgrumbls' : allgrumbls}
		return render(request,'searchResult.html',context)

@login_required
def home(request):
	people = Person.objects.exclude(id =request.user.person.id).all()[:5]
	mygrumbls = Grumbl.objects.filter(person=request.user.person)[::-1]
	followers =  request.user.person.follows.all()
	followersgrumbls = []
	context={}

	form = GrumblForm()
	
	print form

	if request.method == 'POST':
		return add_grumbl(request)

	for follower in followers :
		followersgrumbls+=Grumbl.objects.filter(person=follower)[::-1]

	person = request.user.person
	context = {'mygrumbls':mygrumbls, 'followersgrumbls':followersgrumbls,'person':person,'people':people, 'id':request.user.id,'form':form}

	return render(request,'stream.html',context)

@transaction.atomic
@login_required
def edit_profile(request,id):
	errors = []
	context = {}
	profile_to_edit = get_object_or_404(Person,user=request.user,id=id)
	person = request.user.person
	if request.method =='GET':
		form = EditForm(instance=profile_to_edit)
		context = {'form':form, 'person':person,'id':id}
		return render(request,'editProfile.html',context)
	current_user = request.user
	person = current_user.person
	form = EditForm(request.POST, request.FILES, instance = profile_to_edit)
	if not form.is_valid():
		context = {'form':form, 'person':person,'id':id}
		return render(request,'editProfile.html',context)
	print(form.cleaned_data['password1'])
	
	form.save()
	return redirect(reverse('home'))

@transaction.atomic
@login_required
def change_password(request,id):
	user_to_edit = get_object_or_404(User,id = id)
	person = request.user.person
	errors=[]
	context = []
	form = ChangePasswordForm(request.POST, instance = user_to_edit)
	if request.method =='GET':
		print("ay")
		form = ChangePasswordForm(instance=user_to_edit)
		context = {'form':form, 'user':user_to_edit,'id':id,'person':user_to_edit.person}
		return render(request,'changePassword.html',context)
	if not form.is_valid():
		print("sub")
		context = {'form':form, 'person':person, 'id':id, 'person':person}
		return render(request,'changePassword.html',context)
	old_password = form.cleaned_data['oldPassword']
	if not user_to_edit.check_password(old_password):
		print("here")
		errors.append("old passwrod is incorrect")
		context = {'form':form, 'person':person, 'id':id, 'person':person,'errors':errors}
		return render(request,'changePassword.html',context)
	user_to_edit.set_password(form.cleaned_data['password1'])
	# use set password function

	user_to_edit.save()
	print(user_to_edit)
	print(user_to_edit.password)
	return redirect(reverse('home'))


@transaction.atomic
@login_required
def show_profile(request,id):
	target_user = get_object_or_404(User,id=id)

	target_person = Person.objects.get(user=target_user)
	selfu = request.user.person
	mygrumbls = Grumbl.objects.filter(person=target_person)[::-1]
	print(target_person.picture)
	print (target_person.user)
	print(request.user)
	context = {'target_person':target_person,'mygrumbls':mygrumbls, 'user':request.user,'id':target_user.id, 'person':request.user.person,\
	 'all_followers':selfu.follows.all(), 'all_blocks': selfu.blocks.all(), 'target_user':target_user}
	# if self is blocked by target person
	print ("reach here")
	if selfu in target_person.blocks.all():
		return render(request, 'blocked.html',context)



	return render(request,'viewProfile.html',context)



@transaction.atomic
@login_required
def un_follow(request,id):
	errors =[]
	context = {}
	user_to_unfollow = get_object_or_404(User,id=id)
	person_to_unfollow = Person.objects.get(user=user_to_unfollow)
	mygrumbls = Grumbl.objects.filter(person=person_to_unfollow)[::-1]
	self = request.user.person
	all_followers = self.follows.all()
	self.follows.remove(person_to_unfollow)
	self.save()
	# context = {'person':person_to_unfollow, 'mygrumbls':mygrumbls, 'id':person_to_unfollow.id, 'all_followers':self.follows.all()}
	return show_profile(request,id)


@transaction.atomic
@login_required
def add_follow(request,id):
	errors = []
	context = {}
	user_to_follow = get_object_or_404(User,id=id)
	person_to_follow = Person.objects.get(user=user_to_follow)

	mygrumbls = Grumbl.objects.filter(person=person_to_follow)[::-1]
	self = request.user.person
	print ("hey this is ")
	print (self)

	all_followers = self.follows.all()
	print (all_followers)
	if person_to_follow in self.follows.all():
		return show_profile(request,id)

	print(person_to_follow)
	print(user_to_follow)
	self.follows.add(person_to_follow)
	self.save()
	print(self.follows.all())
	# context = {'person':person_to_follow, 'mygrumbls':mygrumbls, 'id':person_to_follow.id, 'all_followers':self.follows.all()}

	return show_profile(request,id)

@login_required
@transaction.atomic
def block(request,id):
	errors =[]
	context ={}
	user_to_block = get_object_or_404(User,id=id)
	person_to_block = Person.objects.get(user=user_to_block)
	print (person_to_block)
	# remove following
	# add to blocking
	self = request.user.person
	if user_to_block in self.follows.all():
		self.follows.remove(person_to_block)

	self.blocks.add(person_to_block)
	print(id)
	# context = {'person':person_to_block, 'mygrumbls':mygrumbls, 'id':person_to_follow.id, 'all_followers':self.follows.all()}
	return show_profile(request,id)

def un_block(request,id):
	user_to_unblock = get_object_or_404(User,id=id)
	person_to_unblock = Person.objects.get(user=user_to_unblock)
	request.user.person.blocks.remove(person_to_unblock)
	return show_profile(request,id)

@transaction.atomic
@login_required
def add_grumbl(request):
	errors = []
	form = GrumblForm(request.POST,request.FILES)
	if not form.is_valid():
		return redirect(reverse('home'))

	new_grumbl = Grumbl(text=form.cleaned_data['text'], person=request.user.person)
	if form.cleaned_data['picture']:
		new_grumbl.picture = form.cleaned_data['picture']
	new_grumbl.save()
	# person = request.user.person
	mygrumbls = Grumbl.objects.filter(person=request.user.person)[::-1]
	# all_followers = request.user.person.follows.all()
	# followersgrumbls = []
	# for a in all_followers:
	# 	followersgrumbls += Grumbl.objects.filter(person = a)[::-1]
	# context = {'mygrumbls':mygrumbls, 'followersgrumbls':followersgrumbls,'person':person, 'id':person.id}


	return redirect(reverse('home'))
@transaction.atomic
@login_required
def dislike(request,id):
	errors = []
	url = request.POST['page']


	context={}
	person = request.user.person
	mygrumbls = Grumbl.objects.filter(person=request.user.person)[::-1]
	all_followers = request.user.person.follows.all()
	followersgrumbls = []
	for a in all_followers:
		followersgrumbls += Grumbl.objects.filter(person = a)[::-1]
	grumbl = Grumbl.objects.get(id=id)


	context = {'mygrumbls':mygrumbls, 'followersgrumbls':followersgrumbls,'person':person, 'id':request.user.id}
	if (url == "viewProfile.html"): # viewing someone's page need to change the id field
		target_person_id = request.POST['target_person']
		context ['id'] = target_person_id
		
		target_person = Person.objects.get(id=target_person_id)
		context ['target_person'] = target_person
		context ['mygrumbls'] = Grumbl.objects.filter(person=target_person)[::-1]

	if (Dislike.objects.filter(user_id=request.user.id)):
		# remove dislike
		d = Dislike.objects.get(user_id=request.user.id)
		grumbl.dislikes.remove(Dislike.objects.get(user_id=request.user.id))
		d.delete()
		return render(request,url,context)
	
	d = Dislike(user_id=request.user.id)

	d.save()

	grumbl.dislikes.add(d)

	grumbl.save()
	return render(request,url,context)




@transaction.atomic
@login_required
def add_comment(request,id):
	text = request.POST['text']
	errors = []
	context = {}
	url = request.POST['page']
	mygrumbls = Grumbl.objects.filter(person=request.user.person)[::-1]
	all_followers = request.user.person.follows.all()
	followersgrumbls = []
	for a in all_followers:
		followersgrumbls += Grumbl.objects.filter(person = a)[::-1]
	person = request.user.person
	grumbl = Grumbl.objects.get(id=id)
	context = {'mygrumbls':mygrumbls, 'followersgrumbls':followersgrumbls,'person':person, 'id': person.id}
	c=Comment(text=text,person_name= request.user.person.first_name, person=request.user.person)
	c.save()
	grumbl.comments.add(c)
	grumbl.save()
	return render(request,url,context)

@transaction.atomic
@login_required
def delete_grumbl(request, id):
	errors = []
	try:
		grumbl_to_delete = Grumbl.objects.get(id=id, person=request.user.person)
		grumbl_to_delete.delete()
	except ObjectDoesNotExist:
		errors.append('The grumbl does not exist')
	person = request.user.person
	mygrumbls = Grumbl.objects.filter(person=request.user.person)[::-1]
	followersgrumbls =  Grumbl.objects.exclude(person=request.user.person)[::-1]
	context = {'mygrumbls':mygrumbls, 'followersgrumbls':followersgrumbls,'person':person,'id':person.id}
	return redirect(reverse('home'))

@login_required
def get_photo(request, id):
	person = get_object_or_404(Person, user=request.user)
	if not person.picture:
		raise Http404

	content_type = guess_type(person.picture.name)
	return HttpResponse(person.picture, content_type=content_type)

@login_required
def get_grumbl_photo(request,id):
	grumbl = get_object_or_404(Grumbl, id=id)
	if not grumbl.picture:
		raise Http404
	content_type = guess_type(grumbl.picture.name)
	return HttpResponse(grumbl.picture, content_type=content_type)

def forgot_password(request):
	if request.method == 'GET':
		return render(request, 'forgotPassword.html',{})
	errors = []
	username = request.POST['username']
	user = User.objects.get(username=username)
	token = default_token_generator.make_token(user)
	person=user.person
	context = {}
	context ['email_address'] = person.email_address
	email_body = """
	use following toke to reset password:

	  http://%s%s
	""" % (request.get_host(), reverse('confirm_reset', args=(user.username, token)))
	send_mail(subject="Verify your email address",message= email_body,from_email="charlie+devnull@cs.cmu.edu",recipient_list=[person.email_address])

	return render(request,'reset-confirmation.html',context)


def confirm_reset(request,username,token):
	user = get_object_or_404(User,username = username)

		# Send 404 error if token is invalid
	if not default_token_generator.check_token(user, token):
		print token
		raise Http404
	context ={}
		# Otherwise token was valid, activate the user.
	context['user'] = user

	return redirect(reverse('set_password'+'/'+str(user.id)))





def set_password(request,id):
	user = get_object_or_404(User, id=id)
	context = {}
	context['user'] =user
	if request.method =='GET':
		context['form'] = SetPasswordForm()
		return render(request, 'setNewPassword.html',context)
	form = SetPasswordForm(request.POST)
	if not form.is_valid():
		return render(request, 'setNewPassword.html',context)
	user.set_password(form.cleaned_data['password1'])
	login(request, new_user)
	return redirect(reverse('home'))




@transaction.atomic
def register(request):
	context = {}

	# Just display the registration form if this is a GET request
	if request.method =='GET':
		context['form'] = RegistrationForm()
		return render(request, 'registration.html',context)
	errors = []
	context['errors'] = errors
	form = RegistrationForm(request.POST, request.FILES)
	context ['form'] = form

	if not form.is_valid():
		return render(request, 'registration.html',context)

	# Creates the new user from the valid form data
	new_user = User.objects.create_user(username=form.cleaned_data['username'], \
		password=form.cleaned_data['password1'])
	new_user.is_active=False
	new_user.save()
	#do we need to check these manually????
	print(form.cleaned_data['picture'])
	new_user = authenticate(username=form.cleaned_data['username'], \
		password=form.cleaned_data['password1'])

	new_person = Person(first_name=form.cleaned_data['first_name'],last_name=form.cleaned_data['last_name'], \
		email_address=form.cleaned_data['email_address'],description="",user=new_user, picture=form.cleaned_data['picture'])
	new_person.save()

	token = default_token_generator.make_token(new_user)
	email_body = """
	Welcome to Grumbl.  Please click the link below to
	verify your email address and complete the registration of your account:

	  http://%s%s
	""" % (request.get_host(), reverse('confirm', args=(new_user.username, token)))
	send_mail(subject="Verify your email address",message= email_body,from_email="charlie+devnull@cs.cmu.edu",recipient_list=[new_person.email_address])

	context['email_address'] = form.cleaned_data['email_address']



	return render(request,'needs-confirmation.html',context)

@transaction.atomic
def confirm_registration(request, username, token):
	user = get_object_or_404(User, username=username)

		# Send 404 error if token is invalid
	if not default_token_generator.check_token(user, token):
		print token
		raise Http404

		# Otherwise token was valid, activate the user.
	user.is_active = True
	user.save()

	return render(request, 'confirmed.html', {})

def get_mygrumbl(request):
	response_text = serializers.serialize("json",Grumbl.objects.all())
	return HttpResponse(response_text, content_type="application/json")


