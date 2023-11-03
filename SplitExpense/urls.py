from django.urls import path
from .views import *
urlpatterns = [
    path('createuser/', CreateUserView.as_view()),
    path('expenses/', ExpenseAPI.as_view()),
    path('showdetails/', ShowDetails.as_view()),
    # path('expenses/<str:user_id>/', ExpenseAPI.as_view()),
  
]