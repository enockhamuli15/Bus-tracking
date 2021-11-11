from django.urls import path
from .views import *
from django.contrib.auth import views as personnalize

urlpatterns = [
    path('registration/', registration, name='register_now'),
    path('', personnalize.LoginView.as_view(template_name='login.html'), name = 'login_now'),
    path('logout/', personnalize.LogoutView.as_view(template_name='logout.html'), name = 'logout_now'),
    path('buses/', busDetailView, name='buses'),
    path('station/', station, name='stations'),
    
    path('dashboard/', dashboard, name='dashboard'),
    path('drivers/', drivers, name='drivers'),
    path('balance/', balance, name='balance'),
    path('roads/', roads, name='roads'),
    path('users/', passenger, name='passengers'),
    path('records/', records, name='records'),
    path('health/', health, name='health'),
    path('cards/', cards, name='cards'),
    path('new-user/', user, name='user'),
    path('track/', track, name='track'),

    path('update/road/<int:pk>/', RoadUpdateView.as_view(), name='road_update'),
    path('delete/road/<int:pk>/', DeleteRoad.as_view(), name='road_delete'),
    path('update/card/<int:pk>/', CardUpdateView.as_view(), name='card_update'),
    path('delete/card/<int:pk>/', DeleteCard.as_view(), name='card_delete'),
    path('update/station/<int:pk>/', BusStationUpdateView.as_view(), name='station_update'),
    path('delete/station/<int:pk>/', DeleteBusStation.as_view(), name='station_delete'),
    path('update/bus/<int:pk>/', BusUpdateView.as_view(), name='bus_update'),
    path('delete/bus/<int:pk>/', DeleteBus.as_view(), name='bus_delete'),
    path('update/user/<int:pk>/', ProfileUpdateView.as_view(), name='user_update'),
    path('delete/user/<int:pk>/', DeleteProfile.as_view(), name='user_delete'),

    path('user/<cardNum>/', UserDetailView.as_view(), name='user_info'),
    path('increment-on/<int:pk>/', increment, name='incrementation'),
    path('decrement-on/<int:pk>/', decrement, name='decrementation'),
    path('available_sits/<int:pk>/', sits, name='nSits')
]