from django.urls import path
from .views import RequestCodeView, VerifyCodeView, ActivateCodeView, UserListView

urlpatterns = [
    path('auth/request-code/', RequestCodeView.as_view()),
    path('auth/verify-code/', VerifyCodeView.as_view()),
    path('activate-code/', ActivateCodeView.as_view()),
    path('users/', UserListView.as_view()),
]
