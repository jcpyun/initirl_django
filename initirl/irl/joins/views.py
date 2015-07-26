from django.shortcuts import render, HttpResponseRedirect

from .forms import EmailForm, JoinForm

from .models import Join

import uuid

def get_ip(request):
	try:
		x_forward= request.META.get("HTTP_X_FORWARDED_FOR")
		if x_forward:
			ip = x_forward.split(",")[0]
		else:
			 ip = request.META.get("REMOTE_ADDR")
	except:
		ip=""
	return ip

def get_ref_id():
	ref_id= str(uuid.uuid4())[:11].replace('-','').lower()
	try:
		id_exists= Join.objects.get(ref_id=ref_id)
		get_ref_id()
	except:
		return ref_id

def share(request,ref_id):
	context={
		"ref_id" : ref_id,
	}
	template="share.html"
	return render(request,template,context)

def home(request):

	###### print for IP address
	# print request.META.get("REMOTE_ADDR")
	# print request.META.get("HTTP_X_FORWARDED_FOR")
	#########
	##############################################################
	# This is using Regular Django Forms
	##############################################################
	# form = EmailForm(request.POST or None) ## this checks if email is valid 
	# if form.is_valid():
	# 	email=form.cleaned_data['email']
	# 	new_join, created= Join.objects.get_or_create(email=email)
	# 
	####################################################

	####################################################
	#using django forms.py
	####################################################

	form = JoinForm(request.POST or None)
	if form.is_valid():
		new_join = form.save(commit=False)
		#####################################
		## this bottom prevents duplicates ##
		#####################################
		#email=form.cleaned_data['email']
		#new_join_old, created= Join.objects.get_or_create(email=email)
		#new_join.save()
		##################################
		####################################
		# OTHER METHOD. THIS IS REALLY GOOD V V V V V V V V 
		##################
		email=form.cleaned_data['email']
		new_join_old, created= Join.objects.get_or_create(email=email)
		if created:
			new_join_old.ref_id= get_ref_id()  ### THIS GETS REFERENCE ID
			new_join_old.ip_address=get_ip(request)
			new_join_old.save()
		#redirect here
		return HttpResponseRedirect("/%s" %(new_join_old.ref_id))
		######################################
		#### bottom is for ip address.
		######################################
		# new_join.ip_address = get_ip(request)
		# new_join.save()
		######################################
		######################################
	template= "home.html"
	context={
		"form": form
	}
	
	return render(request, template, context)