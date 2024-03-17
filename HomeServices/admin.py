from django.contrib import admin
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib import messages
from . forms import TForm,SForm,ReqForm
from . models import User,ServiceRequest,Feedback,Service,Date
from django import forms
import random
User = get_user_model()

def send_activation_email(modeladmin, request, queryset):
    for user in queryset:
        if not user.is_active:
            if user.gender == '0':
                gender_label = 'Male'
            elif user.gender == '1':
                gender_label = 'Female'
            else:
                gender_label = 'Others'
            if user.role_type == '0':
                occupation_label = 'Carpenter'
            elif user.role_type == '1':
                occupation_label = 'Plumber'
            elif user.role_type == '2':
                occupation_label = 'Electrician'
            else:
                occupation_label = 'Unknown'

            subject = ' Account Activated '
            message = f' Hello {user.username} Your Request has been accepted as Service Provider by the owner.. \n Please Check the details below mentioned \n Details : \n Service Provider Name : {user.uname} \n Username : {user.username} \n Gender : {gender_label} \n Mobile no : {user.phone_no} \n Service Role : {occupation_label} \n Now you can login into your account to accept the services.. Have a great day!!!..'
            print(message)
            from_email = 'missionimpossible4546@gmail.com'  # Replace with your admin's email address
            recipient_list = [user.email]

            try:
                send_mail(subject, message, from_email, recipient_list)
                user.is_active = True
                user.save()
                messages.success(request, f'Activation email sent to {user.username}')
            except Exception as e:
                messages.error(request, f'Error sending email to {user.username}: {str(e)}')

send_activation_email.short_description = "Send activation email and activate selected users"

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    ordering = ('username',)
    actions = [send_activation_email]



class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'role_type', 'uid','date','tflatno', 'tmobile')
    list_filter = ('role_type', 'status')
    actions = ['assign_service_provider']

    def get_queryset(self, request):
        # Customize the queryset here
        qs = super().get_queryset(request)
        qs=ServiceRequest.objects.filter(status="On Progress")
        print(qs)
        # Filter the queryset as needed
        return qs



    def assign_service_provider(self, request, queryset):
        selected_service_requests = queryset.filter(status='On Progress')
        print(queryset)

        # Loop through selected service requests
        for service_request in selected_service_requests:
            # Filter service providers based on the role type of the service request
            service_providers1 = User.objects.filter(user_role='1', role_type=service_request.role_type)
            service_providers=[]
            sd = service_request.date.strftime('%Y-%m-%d')
            for i in service_providers1:
                    d= i.appointement_dates.all()
                    m=[]
                    for j in d:
                        m.append(j.date)
                    print("dates  ",m)
                    print(' request date  ',sd)
                    if sd not in m :
                        service_providers.append(i)
                        print(i)
            if service_providers:
                # For simplicity, here we just assign the first available service provider
                service_provider = random.choice(service_providers)
                print(service_providers,service_provider) 
                #service_provider=Service(instance=service_request)
                # Assign the service provider to the service request
                if service_provider is not None:
                    service_request.service_provideruid = service_provider.username
                    service_request.status = 'Accepted'
                    dat=Date.objects.create(date=sd)
                    service_provider.appointement_dates.add(dat)
                    
                    service_request.save()

                    if service_provider.gender == '0':
                        gender_label = 'Male'
                    elif service_provider.gender == '1':
                        gender_label = 'Female'
                    else:
                        gender_label = 'Others'
                    if service_request.role_type == '0':
                        occupation_label = 'Carpenter'
                    elif service_request.role_type == '1':
                        occupation_label = 'Plumber'
                    elif service_request.role_type == '2':
                        occupation_label = 'Electrician'
                    else:
                        occupation_label = 'Unknown'

                    subject = f' Service Accepted {service_request.role_type}'
                    message = f' Hello {service_request.uid.username} Your  Service Request has been accepted.. \n PLEASE CHECK THE DETAILS : \n Flat No : {service_request.tflatno} \n Contact No : {service_request.tmobile} \n Date : {service_request.date} \n Service Type : {occupation_label} \n SERVICE PROVIDER DETAILS : \n Service Provider Name : {service_provider.uname} \n Gender : {gender_label} \n Mobile no : {service_provider.phone_no} \n Please mention the feedback after completion of service in the site.. Have a great day!!!..'
                    print(message)
                    from_email = 'missionimpossible4546@gmail.com'  # Replace with your admin's email address
                    recipient_list = [service_request.uid.email]

                    try:
                        send_mail(subject, message, from_email, recipient_list)
                        messages.success(request, f' email sent to {service_request.uid.username}')
                    except Exception as e:
                        messages.error(request, f'Error sending email to {service_request.uid.username}: {str(e)}')

                    subject = f' NEW SERVICE APPOINTEMENT'
                    message = f' Hello {service_provider.username} You have got a new service appointement..\n PLEASE CHECK THE DETAILS : \n customer name : {service_request.uid.uname} \n  customer mobile : {service_request.tmobile} \n Requested Service : {occupation_label} \n Flat No : {service_request.tflatno} \n Date : {service_request.date} \n Hope you give a better service and mention the completion status after feedback completed.. Have a great day!!!..'
                    print(message)
                    from_email = 'missionimpossible4546@gmail.com'  # Replace with your admin's email address
                    recipient_list = [service_provider.email]

                    try:
                        send_mail(subject, message, from_email, recipient_list)
                        messages.success(request, f' email sent to {service_provider.username}')
                    except Exception as e:
                        messages.error(request, f'Error sending email to {service_provider.username}: {str(e)}')



                    self.message_user(request, f'{len(selected_service_requests)} service provider found')
            else:
                # If no service providers are available, set the status to 'Declined'
                service_request.status = 'Declined'
                service_request.save()
                if service_request.role_type == '0':
                    occupation_label = 'Carpenter'
                elif service_request.role_type == '1':
                    occupation_label = 'Plumber'
                elif service_request.role_type == '2':
                    occupation_label = 'Electrician'
                else:
                    occupation_label = 'Unknown'
                subject = f' Service Declined {service_request.uid.username}'
                message = f' Hello {service_request.uid.username} Your  Service Request has been Declined.. Due to No service providers are available for the service {occupation_label} on the date {service_request.date} \n Sorry for the inconvience \n Kindly requesting you to reshedule the appointement   \n  Have a great day!!!..'
                print(message)
                from_email = 'missionimpossible4546@gmail.com'  # Replace with your admin's email address
                recipient_list = [service_request.uid.email]
                send_mail(subject, message, from_email, recipient_list)
                messages.success(request, f' email sent to {service_request.uid.username}')

                print('____________service declined____________')
                self.message_user(request, f'{len(selected_service_requests)} service provider not found')
        
        self.message_user(request, f'{len(selected_service_requests)} service requests processed.')

    assign_service_provider.short_description = 'Assign selected service requests to service providers'


    

    def display_service_providers(self, obj):
        # Retrieve the service providers available for this service request
        service_providers1 = User.objects.filter(user_role='1', role_type=obj.role_type)
        service_providers=[]
        sd = obj.date.strftime('%Y-%m-%d')
        print(sd)
        for i in service_providers1:
            d= i.appointement_dates.all()
            m=[]
            for j in d:
                m.append(j.date)
                print("dates  ",m)
                print(' request date  ',sd)
                if sd not in m :
                    service_providers.append(i.username)
                    print(i.username)
        if service_providers:
            return ','.join(service_providers)

    display_service_providers.short_description = 'Service Providers'




class ServiceAdmin(admin.ModelAdmin):
    list_filter = ('srid__uid__uname','srid__date','srid__role_type','srid__service_provideruid','srid__status')  # Use double underscore to access related model's attribute

    list_display = ('id','tenant_name','tenant_flatno','date','role_type','service_provideruid','tenant_confirmation','provider_confirmation','status','feedback','feedback_status','feedback_description')

    def status(self, obj):
        return obj.srid.status

    status.short_description = 'Status'  # Set a user-friendly name for the column

    def provider_confirmation(self, obj):
        if obj.srid.provider_conf == True:
            return 'completed'
        elif obj.srid.provider_conf == False:
            return 'Not completed'
        else:
            return 'NOt RESPONDED'
    def tenant_confirmation(self, obj):
        if obj.srid.tenant_conf == True:
            return 'completed'
        elif obj.srid.tenant_conf == False:
            return 'Not completed'
        else:
            return 'NOt RESPONDED'

    def tenant_name(self, obj):
        return obj.srid.uid.username

    def tenant_flatno(self, obj):
        return obj.srid.tflatno

    def date(self, obj):
        return obj.srid.date

    def service_provideruid(self, obj):
        return obj.srid.date
    def feedback(self, obj):
        if obj.srid.feedback_id == '':
            return 'GIVEN'
        else:
            return 'NOT GIVEN'
    def feedback_status(self, obj):
        if obj.srid.feedback_id == '':
            return '--'
        else:
            f=Feedback.objects.get(id=obj.srid.feedback_id)
            if f.satisfaction == '0':
                return 'Excelent'
            elif f.satisfaction == '1':
                return 'Good'
            else:
                return 'Bad'
    def feedback_description(self, obj):
        if obj.srid.feedback_id == '':
            return '--'
        else:
            f=Feedback.objects.get(id=obj.srid.feedback_id)
            return f.description



    status.short_description = 'Status'  # Set a user-friendly name for the column

    def role_type(self, obj):
        if obj.srid.role_type == '0':
            return 'Carpenter'
        elif obj.srid.role_type == '1':
            return 'Plumber'
        else:
            return 'Electrician'

 

admin.site.register(Service, ServiceAdmin)
admin.site.register(ServiceRequest, ServiceRequestAdmin)
admin.site.register(Date)



admin.site.register(User, CustomUserAdmin)
admin.site.register(Feedback)
