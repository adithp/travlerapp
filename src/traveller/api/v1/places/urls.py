from django.urls import path
from api.v1.places import views

urlpatterns = [
    path('',views.places),
    path('view/<int:pk>',views.place),
    path('protected/<int:pk>',views.protected),
    path('comments/<int:pk>/',views.comments),
    path('comments/create/<int:pk>/',views.comment_create),
]
