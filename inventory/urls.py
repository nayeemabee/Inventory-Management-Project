from django.urls import path
from .views import get_item_list, create_item, item_detail


urlpatterns = [
    path('items/', create_item, name='create_item'),  
    path('item-list/', get_item_list, name='get_item_list'),  
    path('items/<int:item_id>/', item_detail, name='item_detail'), 
]
