from django.conf.urls import url
from www.views import LoginView, LogoutView, ScoreView, RegisterView

urlpatterns = [
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^register/', RegisterView.as_view(), name='register'),
    url(r'^logout/', LogoutView.as_view(), name='logout'),
    url(r'^scoreboard/', ScoreView.as_view(), name='scoreboard')
]