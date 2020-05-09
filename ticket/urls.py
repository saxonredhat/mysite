from django.urls import path
from .views import *

app_name = "ticket"
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('add', TicketCreateView.as_view(), name='create'),
    path('list', TicketListView.as_view(), name='list'),
    path('tome', TicketToMeListView.as_view(), name='list'),
    path('detail/<int:pk>', TicketDetailView.as_view(), name='detail'),
    path('update/<int:pk>', TicketUpdateView.as_view(), name='update'),

]