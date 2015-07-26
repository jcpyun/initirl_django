from django.conf import settings

from django.shortcuts import render, HttpResponseRedirect, Http404

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
	try:
		join_obj=Join.objects.get(ref_id=ref_id)
		friends_referred= Join.objects.filter(friend=join_obj)
		count= join_obj.referral.all().count()
		#ref_url= "http://initirl.com/?ref=%s" %(join_obj.ref_id) #### REFERENCE URL
		ref_url=settings.SHARE_URL + str(join_obj.ref_id)
		context={"ref_id" : join_obj.ref_id, "count": count, "ref_url": ref_url}
		template="share.html"
		return render(request,template,context)
	# except Join.DoesNotExist:
	# 	raise Http404
	except:
		raise Http404

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

	####################################################
	################# MIDDLEWARE IS BELOW ###############
	try:
		join_id=request.session['join_id_ref']
		obj= Join.objects.get(id=join_id)
		#print "the obj is %s" %(obj.email)
	except:
		obj= None
	
	################## MIDDLEWARE IS ABOVE #############
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
			if not obj== None:
				new_join_old.friend= obj ############## Refereral Friend. 
			new_join_old.ip_address=get_ip(request)
			new_join_old.save()

		#print all "friends" ("invited_by") that joined as a result of main sharer email
		#print Join.objects.filter(friend=obj)#.count()  ## MIGHT HAVE TO COMMENT
		#print obj.referral.all()#.count()				## MIGHT HAVE TO COMMENT

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