from django.urls import path
from .views import *

app_name = "ticket"
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('add', TicketCreateView.as_view(), name='create'),
    path('add/from/<int:ticket_id>/to/<str:space_code>', TicketCreateFromTicketView.as_view(), name='create_from_ticket'),
    path('bind', ticket_bind_info, name='bind'),
    path('list', TicketListView.as_view(), name='list'),
    path('tome', TicketToMeListView.as_view(), name='to_me_list'),
    path('detail/<int:pk>', TicketDetailView.as_view(), name='detail'),
    path('update/<int:pk>', TicketUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', TicketDeleteView.as_view(), name='delete'),
    path('cancel/<int:pk>', TicketCancelUpdateView.as_view(), name='cancel'),
    path('audit/<int:pk>', TicketAuditUpdateView.as_view(), name='audit'),
    path('execute/<int:pk>', TicketExecuteUpdateView.as_view(), name='execute'),
    path('test/<int:pk>', TicketTestUpdateView.as_view(), name='test'),
]