from django.urls import path

from . import views
# localhost:8000/linked/2
urlpatterns = [
    path('', views.index, name='index'),                                    # Home page
    path('login/', views.login, name='login'),                              # Login page
    path('signup/', views.signup, name='signup'),                           # Registration page
    path('logout/', views.logout, name='logout'),                           # Logout endpoint
    path('profile/', views.profile, name='profile'),                        # Own profile page
    path('new/', views.new, name='new'),                                    # Own profile page
    path('category/new/', views.new_category, name='newcat'),               # Category New
    path('profile/<str:username>/', views.profile, name='profile'),         # Other profile page
    path('<int:link_id>/', views.detail, name="detail"),                    # Link detail
    path('redirect/<int:link_id>/', views.redirect, name="redirect"),       # Redirection
]

