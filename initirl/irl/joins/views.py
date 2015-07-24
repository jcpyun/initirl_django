from django.shortcuts import render
from .forms import EmailForm

def home(request):
	form = EmailForm()
	template= "home.html"
	context={
		"form": form
	}
	return render(request, template, context)