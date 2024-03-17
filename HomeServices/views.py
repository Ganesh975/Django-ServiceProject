from django.shortcuts import render,redirect
from . forms import TForm,SForm,ReqForm,FedForm
from . models import User,ServiceRequest,Feedback,Service,Date
from django.contrib import messages
from django.contrib.auth.models import auth
from django.shortcuts import render
from .utils import send_notification_email
from django.db.models import Q
from datetime import date, timedelta
import os
import datetime

def home(request):
	k=['carpenter.webp','plumber.jpeg','electricain.jpeg','waterservice.jpeg','cleaning.jpeg']
	t={'Carpenter','Plumber','Electrician','Water Service','Cleaning'}
	image_folder = 'static/images'
	image_info_list = []
	for filename in os.listdir(image_folder):
		if filename.endswith('.jpeg') or filename.endswith('.png') or filename.endswith('.webp'):
			image_url = os.path.join(image_folder, filename)
			title = filename.replace('.jpg', '').replace('.png', '')
			if title in k:
				print(title,image_url)
				image_info = {
					'image_url': image_url,
					'title': title,
					}
				image_info_list.append(image_info)
	context = {
		'image_info_list': image_info_list,
	}
	print(image_info_list)
	return render(request, 'html/home.html', {'image_info_list':image_info_list,'titles':t})


def tlogin(request):
	if request.method=="POST":
		uid=request.POST.get('username','')
		password=request.POST.get('password','')
		print(uid,password)
		user=auth.authenticate(request,username=uid,password=password)
		print(user)
		if user is not None:
			print("user successful")
			auth.login(request,user)
			return redirect("/")
		else:
			print(" unsuccessful ")
			messages.info(request,'invalid credentials')
			return redirect("tlogin")
	else:	
		return render(request,'html/User_Login.html')


def tregister(request):
    if request.method == "POST":
    	g=TForm(request.POST)
    	if g.is_valid():
    		g.save()
    		print("user created")
    		uid=request.POST.get('username','')
    		password=request.POST.get('password1','')
    		u = User.objects.get(username=uid)
    		u.user_role = '0'
    		u.save()
    		print(uid,password)
    		user=auth.authenticate(request,username=uid,password=password)
    		print(user)
    		if user is not None:
    			print("user successful")
    			auth.login(request,user)
    			return redirect("/")
    		else:
    			print(" unsuccessful ")
    			messages.info(request,'invalid credentials')
    		return redirect('home')
    	else:
    		print("user not created")
    		messages.info(request,'please give valid credentials')
    		print(g.errors)
    g=TForm()
    g.user_role='0'
    return render(request,'html/User_registration.html',{'form':g})

def tlogout(request):
	auth.logout(request)
	return redirect('home')


def sregister(request):
    if request.method == "POST":
    	g=SForm(request.POST, request.FILES)
    	if g.is_valid():
    		g.save()
    		print("user created")
    		uid=request.POST.get('username','')
    		password=request.POST.get('password1','')
    		u = User.objects.get(username=uid)
    		
    		u.save()
    		u = g.save(commit=False)
    		u.user_role='1'
    		u.is_active = False 
    		u.save()

    		send_email_to_admin(request,u)
    		messages.info(request,'Request set successfully')
    		print(uid,password)

    	else:
    		print("user not created")
    		messages.info(request,'please give valid credentials')
    		print(g.errors)
    g=SForm()
    g.user_role='1'
    return render(request,'html/serviceprovider_register.html',{'form':g})

def slogin(request):
	if request.method=="POST":
		uid=request.POST.get('username','')
		password=request.POST.get('password','')
		print(uid,password)

		u = User.objects.get(username=uid)

		if u is not None and not u.is_active:
			messages.info(request,'request doesnot accepted by admin')
		else:
			user=auth.authenticate(request,username=uid,password=password)
			print(user)
			if user is not None:
				if u.user_role=='1':
					auth.login(request,user)
					return redirect("/")
				else:
					messages.info(request,'enter valid username or password')
			else:
				print(" unsuccessful ")
				messages.info(request,'invalid credentials')
		return redirect("slogin")
	else:
		return render(request,'html/Serviceprovider_login.html')


def send_email_to_admin(request,u):
	if u.gender == '0':
		gender_label = 'Male'
	elif u.gender == '1':
		gender_label = 'Female'
	else:
		gender_label = 'Others'
	if u.role_type == '0':
		occupation_label = 'Carpenter'
	elif u.role_type == '1':
		occupation_label = 'Plumber'
	elif u.role_type == '2':
		occupation_label = 'Electrician'
	else:
		occupation_label = 'Unknown'
	subject = ' New Service Provider Requesting For service '
	message = f' User Name {u.username} Has Requested you to join as service Provider in our appatements \n Details : \n Service Provider Name : {u.uname} \n Username : {u.username} \n Gender : {gender_label} \n Mobile no : {u.phone_no} \n Service Role : {occupation_label} \n if you want to accept the request then login and accept'
	print(message)
	from_email = 'missionimpossible4546@gmail.com'  # Sender's email
	recipient_list = ['missionimpossible4546@gmail.com']  # List of recipient email addresses
	send_notification_email(subject, message, from_email, recipient_list)
	return render(request, 'html/home.html')


def aboutus(request):
	return render(request,'html/Aboutus.html')

def contactus(request):
	return render(request,'html/contactus.html')



def requesting_service(request):
	query = Q(status='On Progress')
	h = ServiceRequest.objects.filter(uid_id=request.user.id).filter(query)
	if request.method == "POST":
		t = ReqForm(request.POST)
		if t.is_valid():
			c = t.save(commit=False)
			c.uid_id = request.user.id
			c.tflatno = request.user.tflatno
			c.save()
			s=Service()
			print(c.id)
			s.srid_id=c.id
			s.save()
			messages.info(request,'request sent')
			return redirect('requesting_service')
		messages.info(request,'please give valid credentials')
		print(t.errors)
	t = ReqForm()
	return render(request,'html/requesting_service.html',{'w':t,'s':h})


def upcoming_services(request):
	d=datetime.datetime.now()
	date=d.date()
	yesterday = date.today() - timedelta(days=1)
	print(yesterday)
	query = Q(status='Accepted') | Q(status='UnAccomplished', date=yesterday) | Q(status='Service Completed',date=yesterday)
	h = ServiceRequest.objects.filter(uid_id=request.user.id).filter(query)
	combined_data=[]
	
	
	for j in h:
		p=None
		print(j.service_provideruid)
		p= User.objects.get(username=j.service_provideruid)
		print(p)
		combined_data.append({'service':j, 'provider': p})
		print(combined_data)
	combined_data.append({'sid': 'your_sid_value_here'})
	return render(request,'html/upcoming_services.html',{'combined_data':h,'d':date})
def profile(request,sid):
	k=User.objects.get(username = sid)
	print("hi",k)
	return render(request,'html/profile.html',{'s':k})
	
def feedback(request,sid):
	if request.method == "POST":
		t = FedForm(request.POST)
		if t.is_valid():
			u=ServiceRequest.objects.get(id=sid)
			c = t.save(commit=False)
			c.provider_uid = u.service_provideruid
			c.tid = request.user.username
			c.feedback=True
			c.service_id=u.id
			c.save()
			u.feedback_id=c.id
			c.save()
			u.save()
			messages.info(request,'')
			return redirect('upcoming_services')
		messages.info(request,'please give valid credentials')
		print(t.errors)
	u=ServiceRequest.objects.get(id=sid)
	s=User.objects.get(username=u.service_provideruid)
	print(s)
	f=FedForm()
	return render(request,'html/feedback.html',{'u':u,'s':s,'form':f})

def appointements(request):
	d=datetime.datetime.now()
	date=d.date()
	yesterday = date.today() - timedelta(days=1)
	print(yesterday)
	query = Q(status='Accepted') | Q(status='UnAccomplished', date=yesterday)
	h = ServiceRequest.objects.filter(service_provideruid=request.user.username).filter(query)
	print(h)
	d=datetime.datetime.now()
	date=d.date()
	print(d,date)
	return render(request,'html/appointements.html',{'h':h,'d':date})
def cmp(request, item_id):
	h = ServiceRequest.objects.get(id=item_id)
	h.provider_conf=True
	h.save()
	subject = f' Service Completed PLease Confirm'
	message = f' Hello {h.uid.username} Your  Service has completed.. \n PLEASE CONFIRM THE SERVICE \n And you may give Review on the service for the service providern {h.service_provideruid} on the portal \n Have a great day!!!..'
	print(message)
	u=User.objects.get(username=h.service_provideruid)
	sd = h.date.strftime('%Y-%m-%d')
	date_obj = Date.objects.get(date=sd)
	u.appointement_dates.remove(date_obj)
	date_obj.delete()
	u.save()
	print(u.appointement_dates.all())
	from_email = 'missionimpossible4546@gmail.com'  # Replace with your admin's email address
	recipient_list = [h.uid.email]
	try:
		send_notification_email(subject, message, from_email, recipient_list)
		print('success',recipient_list)
		messages.success(request, f' email sent to {h.uid.username}')
	except Exception as e:
		print('failed',recipient_list)
		messages.error(request, f'Error sending email to {h.uid.username}: {str(e)}')
		print(e)
	return redirect('appointements')

def notcmp(request, item_id):
    h = ServiceRequest.objects.get(id=item_id)
    h.provider_conf=False
    h.tenant_conf=False
    h.status='UnAccomplished'
    h.save()
    u=User.objects.get(username=h.service_provideruid)
    sd = h.date.strftime('%Y-%m-%d')
    date_obj = Date.objects.get(date=sd)
    u.appointement_dates.remove(date_obj)
    u.save()
    date_obj.delete()
    print(u.appointement_dates.all())
    subject = f' Service UnAccomplished '
    message = f' Hello {h.uid.username} Your  Service has not completed.. \n Sorry for inconvience !!! \n Requesting you to reshedule the service you required on the portal \n Have a great day!!!..'
    print(message)
    from_email = 'missionimpossible4546@gmail.com'  # Replace with your admin's email address
    recipient_list = [h.uid.email]
    try:
    	send_notification_email(subject, message, from_email, recipient_list)
    	messages.success(request, f' email sent to {h.uid.username}')
    	print('success',recipient_list)
    except Exception as e:
    	messages.error(request, f'Error sending email to {h.uid.username}: {str(e)}')
    	print('failed',recipient_list)
    	print(e)
    return redirect('appointements')

def tcmp(request, item_id):
	h = ServiceRequest.objects.get(id=item_id)
	h.provider_conf=True
	h.tenant_conf=True
	h.status='Service Completed'
	h.save()
	u=User.objects.get(username=h.service_provideruid)
	sd = h.date.strftime('%Y-%m-%d')
	date_obj = Date.objects.get(date=sd)
	u.appointement_dates.remove(date_obj)
	date_obj.delete()
	u.save()
	print(u.appointement_dates.all())
	'''
	subject = f' Service Completed '
	message = f' Hello {h.uid.username} Your  Service has completed.. \n And you may give feedback on the service for the service providern {h.service_provideruid} on the portal \n Have a great day!!!..'
	print(message)
	from_email = 'missionimpossible4546@gmail.com'  # Replace with your admin's email address
	recipient_list = [h.uid.email]
	try:
		send_notification_email(subject, message, from_email, recipient_list)
		print('success',recipient_list)
		messages.success(request, f' email sent to {h.uid.username}')
	except Exception as e:
		print('failed',recipient_list)
		messages.error(request, f'Error sending email to {h.uid.username}: {str(e)}')
		print(e)
	'''
	return redirect('upcoming_services')

def tnotcmp(request, item_id):
	h = ServiceRequest.objects.get(id=item_id)
	h.tenant_conf=False
	h.status='UnAccomplished'
	h.save()
	u=User.objects.get(username=h.service_provideruid)
	sd = h.date.strftime('%Y-%m-%d')
	date_obj = Date.objects.get(date=sd)
	u.appointement_dates.remove(date_obj)
	u.save()
	date_obj.delete()
	print(u.appointement_dates.all())
	if h.provider_conf is None:
		subject = f' Service UnAccomplished '
		message = f' Hello {h.service_provideruid} Your  Service Appointement with {h.uid.uname} on date {h.date} has not completed.. \n This makes inconvience for the Tenant which makes bad review on your work \n Asking you to contact the Manager '
		print(message)
		from_email = 'missionimpossible4546@gmail.com' 
		s=User.objects.get(username=h.service_provideruid) # Replace with your admin's email addres
		recipient_list = [s.email]
		send_notification_email(subject, message, from_email, recipient_list)
		messages.success(request, f' email sent to {s.username}')
		print('success',recipient_list)
		return redirect('upcoming_services')
	elif h.provider_conf == True:
		subject = f' Service UnAccomplished '
		message = f' Hello {h.service_provideruid} Your  Service Appointement with {h.uid.uname} on date {h.date} has not completed which is claimed by the tenant..  \n This makes inconvience for the Tenant which makes bad review on your work \n Asking you to contact the tenant and solve the issue... '
		print(message)
		from_email = 'missionimpossible4546@gmail.com'  # Replace with your admin's email addres
		s=User.objects.get(username=h.service_provideruid) # Replace with your admin's email addres
		recipient_list = [s.email]
		send_notification_email(subject, message, from_email, recipient_list)
		messages.success(request, f' email sent to {s.username}')
		print('success',recipient_list)
	return redirect('upcoming_services')

def ratings(request):
	u=request.user.username
	f=Feedback.objects.filter(provider_uid=request.user.username)
	print(f)
	combined_data=[]
	for feedback in f:
		print(feedback.tid)
		user_object=None
		service_object=None
		user_object = User.objects.get(username=feedback.tid)
		service_object=ServiceRequest.objects.get(id=feedback.service_id)
		combined_data.append({'feedback': feedback, 'user': user_object,'service':service_object})
		print(feedback,user_object,service_object)
		print(combined_data)
	return render(request, 'html/ratings.html', {'combined_data': combined_data})
