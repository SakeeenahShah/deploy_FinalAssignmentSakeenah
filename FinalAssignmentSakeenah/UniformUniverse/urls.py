from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.index, name="index"),

    #Sign Up
    path('sign_up/', views.sign_up, name="sign_up"),
    path('sign_up/sign_in/',views.sign_in, name="sign_in"),

    #Direct Sign In from Index
    path('sign_in/', views.sign_in_page, name='sign_in_page'),

    path('sign_in/', auth_views.LoginView.as_view(template_name='sign_in.html'), name='sign_in'),
    path('sign_out/', auth_views.LogoutView.as_view(next_page='homepage'), name='sign_out'),

    #Homepage
    path('homepage/', views.homepage, name="homepage"),
    path('homepage/checkout/<str:uniform_id>/', views.checkout, name='checkout'),
    path('checkout/myorder/', views.myorder, name='myorder'),
    path('myorder/review/<int:order_id>/', views.review_detail, name='review_detail'), 
    path('search_order/', views.search_order, name='search_order'),
    path('search_uniform', views.search_uniform, name="search_uniform"),
    path('review_detail/delete_review/<int:order_id>/', views.delete_review, name='delete_review'),

    # Profile
    path('homepage/profile/', views.profile, name="profile"),
    path('profile/update_customername/', views.update_customername, name='update_customername'),
    path('profile/update_phoneno/', views.update_phoneno, name='update_phoneno'),
    path('profile/update_address/', views.update_address, name='update_address'),
    path('profile/delete_account/', views.delete_account, name='delete_account'),

    # Update and Delete Order
    path('myorder/update_order_address/<int:order_id>/', views.update_order_address, name='update_order_address'),
    path('myorder/delete_order/<int:order_id>/', views.delete_order, name='delete_order'),

    #Review
    path('UniformUniverse/uniform_reviews/<str:uniform_id>/', views.uniform_reviews, name='uniform_reviews')

]