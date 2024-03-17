from django.db import models
from django.contrib.auth.models import AbstractUser 


# Create your models here.

class Date(models.Model):
	date=models.CharField(max_length=100)

class User(AbstractUser):
		
		gender_choices = [
						    ('0','male'),
						    ('1','female'),
						    ('2','others'),
						  ]
		gender = models.CharField(max_length=6,choices=gender_choices,default='0')
		uname=models.CharField(max_length=20)
		tflatno=models.CharField(max_length=30,blank=True)
		phone_no=models.CharField(max_length=10)
		password=models.CharField(max_length=200)
		c = [
			('0','Carpenter'),
			('1','Plumber'),
			('2','Electrician'),
		]
		role=[
			('0','Tenant'),
			('1','ServiceProvider')
		]
		user_role=models.CharField(max_length=6,choices=role,default='0')
		role_type = models.CharField(max_length=8,choices=c,default='0',blank=True)
		provider_photo = models.ImageField(upload_to='photos/', blank=True, null=True)
		appointement_dates=models.ManyToManyField(Date)
class ServiceRequest(models.Model):
	c = [
			('0','Carpenter'),
			('1','Plumber'),
			('2','Electrician'),
		]
	role_type = models.CharField(max_length=8,choices=c,default='Carpenter',blank=True)
	tflatno = models.CharField(max_length=100)
	tmobile = models.IntegerField()
	uid = models.ForeignKey(User,on_delete=models.CASCADE)
	date = models.DateField(default=None, null=True, blank=True)
	
	s = [
			('0','Service Completed'),
			('1','On Progress'),
			('2','Accepted'),
			('3','Declined'),
		]
	status=models.CharField(max_length=8,choices=s,default='On Progress')
	service_provideruid=models.CharField(max_length=100,blank=True)
	feedback_id=models.CharField(max_length=20,blank=True)
	provider_conf=models.BooleanField(default=None,blank=True)
	tenant_conf=models.BooleanField(default=None,blank=True)



class Service(models.Model):
	srid=models.ForeignKey(ServiceRequest,on_delete=models.CASCADE)

class Feedback(models.Model):
	feedback=models.BooleanField(default=False)
	c = [
			('0','Excelent'),
			('1','Good'),
			('2','Bad'),
		]
	satisfaction=models.CharField(max_length=100,choices=c,blank=True)
	description=models.CharField(max_length=200,blank=True)
	provider_uid=models.CharField(max_length=20,blank=True)
	tid=models.CharField(max_length=10,blank=True)
	service_id=models.CharField(max_length=10,blank=True)



		
		





