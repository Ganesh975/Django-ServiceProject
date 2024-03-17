from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as ad
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home,name="home"),
    path('tlogin',views.tlogin,name="tlogin"),
    path('tregister',views.tregister,name='tregister'),
    path('tlogout',views.tlogout,name="tlogout"),
    path('tlogin',views.tlogin,name="tlogin"),
    path('sregister',views.sregister,name='sregister'),
    path('tlogout',views.tlogout,name="tlogout"),
    path('slogin',views.slogin,name='slogin'),
    path('aboutus',views.aboutus,name='aboutus'),
    path('contactus',views.contactus,name='contactus'),
    path('requesting_service',views.requesting_service,name="requesting_service"),
    path('upcoming_services',views.upcoming_services,name="upcoming_services"),
    path('profile/<str:sid>',views.profile,name="profile"),
    path('feedback/<int:sid>',views.feedback,name='feedback'),
    path('appointements',views.appointements,name='appointements'),
    path('cmp/<int:item_id>/', views.cmp, name='cmp'),
    path('notcmp/<int:item_id>/', views.tnotcmp, name='tnotcmp'),
    path('tcmp/<int:item_id>/', views.tcmp, name='tcmp'),
    path('tnotcmp/<int:item_id>/', views.notcmp, name='notcmp'),
    path('ratings',views.ratings,name='ratings')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)