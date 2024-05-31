from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # auth
    path('login/', views.loginPage, name = 'login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),

    path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name='room'),
    path('create-room/', views.createRoom, name='create-room'),
    path('edit-room/<str:pk>/', views.editRoom, name="edit-room"),
    path('delete/<str:pk>/', views.deleteRoom, name="delete"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),

    path('profile/<str:pk>/', views.userProfile, name='user-profile'),
    path('edit-profile/<str:pk>/', views.editProfile, name='edit-profile'),

    path('topics/', views.topics, name="m_topics"),
    path('activity/', views.activity, name="m_activity"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)