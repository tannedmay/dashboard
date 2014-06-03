# Create your views here.
from django.views.decorators.cache import cache_control
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from graphite import models
import random
import string
import pika
import sys
import psutil

def account(request):
	if 'userid' in request.session:
		graphite_url='http://'+request.session['virtual_ip'] 
		if(models.users.objects.filter(id = request.session['userid'])):
	      		user_object = models.users.objects.get(id = request.session['userid'])
	      		api_key=user_object.api
		return render(request, 'account.html', {'logged_in':True, 'api':api_key,'graphite_url':graphite_url})
	else:
		return HttpResponseRedirect('/login/')			

def home(request):
	logged_in=False
	graphite_url=''
	if 'userid' in request.session:
		logged_in=True
		graphite_url='http://'+request.session['virtual_ip']
	return render(request, 'home.html',{'logged_in':logged_in,'graphite_url':graphite_url})

def docs(request):
	logged_in=False
	graphite_url=''
	if 'userid' in request.session:
		logged_in=True
		graphite_url='http://'+request.session['virtual_ip']
	return render(request, 'docs.html',{'logged_in':logged_in,'graphite_url':graphite_url})

def register(request):
    if 'userid' in request.session:
	return HttpResponseRedirect('/account/')			
    errors = {}
    if request.method == 'POST':
        if not request.POST.get('name'):
            errors['name']=' You can\'t leave name empty. '
	else:
	    fn = request.POST.get('name')
	    fn = fn.lower()
        if request.POST.get('email') and '@' in request.POST['email']:
	    eml = request.POST.get('email')
	    if  models.users.objects.filter(email = eml):
	        errors['email']=' This email is already in use. '
	else:
            errors['email']=' Enter a valid e-mail address. '
	if  request.POST.get('password1'):
	    pwd = request.POST.get('password1')
	    if  request.POST.get('password2'):
		cpwd = request.POST.get('password2')
		if(cpwd != pwd):
            	    errors['password']=' Password missmatch. '
	    else:
            	errors['password']=' You can\'t leave password empty. '
	else:
            errors['password']=' You can\'t leave password empty. '
        if not errors:
	    char_set = string.ascii_uppercase + string.digits+string.ascii_lowercase
	    api_key=''.join(random.sample(char_set*500,30))
	    while models.users.objects.filter(api = api_key):
		api_key=''.join(random.sample(char_set*500,30))
	    p = models.users.objects.create( name = fn,
		email = eml ,
		password = pwd ,
	        api = api_key )
	    connection = pika.BlockingConnection(pika.ConnectionParameters(host='10.21.72.39'))
	   # connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	    channel = connection.channel()
	    channel.queue_declare(queue='main_queue', durable=True)
	    message = str(p.id)
	    channel.basic_publish(exchange='',routing_key='main_queue',body=message,properties=pika.BasicProperties(delivery_mode = 2,))
	    print " [x] Sent %r" % (message,)
            connection.close()
            return render (request,'registered.html')
    else:
    	return render(request, 'register.html',{'errors': errors})
    return render(request, 'register.html',{'errors': errors, 'name':request.POST.get('name',''), 'email':request.POST.get('email','')})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login(request):
    if 'userid' in request.session:
    	return HttpResponseRedirect('/account/')			
    if request.method == 'POST':
	if request.session.test_cookie_worked():
	    request.session.delete_test_cookie()
    	    email_from_form = request.POST.get('email')
	    if(models.users.objects.filter(email = email_from_form)):
	      p = models.users.objects.get(email = email_from_form)
	      if request.POST.get('password'):
	    	a = request.POST.get('password')
	        if (p.password == a):
		    request.session['userid'] = p.id
		    request.session['virtual_ip']=p.vip
		    #request.session['virtual_ip']='www.google.com'
	            return HttpResponseRedirect('/account/')
        else:
	   return  HttpResponse("Please enable cookies and try again.")
    else:
	request.session.set_test_cookie()
	return render(request, 'login.html', {'error': False})
    return render(request, 'login.html', { 'error': True, 'email':request.POST.get('email','') })

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
	try:
		del request.session['userid']
	except KeyError:
		pass
	return HttpResponseRedirect('/login/')	
