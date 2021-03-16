from django.urls import path
from app import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # path('', views.home),
    path('', views.ProductView.as_view(), name='home'),
    # path('product-detail/', views.product_detail, name='product-detail'),
    path('product-detail/<int:pk>/',
         views.ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),

    path('cart/', views.show_cart, name='showcart'),
    path('pluscart/', views.plus_cart, name='pluscart'),
    path('minuscart/', views.minus_cart, name='minuscart'),
    path('removecart/', views.remove_cart, name='removecart'),

    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.profile, name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),

    path('changepassword/', views.changePassword, name='changepassword'),

    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>/', views.mobile, name='mobiledata'),

    path('laptop/', views.laptop, name='laptop'),
    path('laptop/<slug:data>/', views.laptop, name='laptopdata'),

    path('bottomwear/', views.bottomWear, name='bottomwear'),
    path('bottomwear/<slug:data>/', views.bottomWear, name='bottomweardata'),

    path('topwear/', views.topWear, name='topwear'),
    path('topwear/<slug:data>/', views.topWear, name='topweardata'),

    path('login/', views.loginPage, name='login'),
    path('logout/', views.logOut, name='logout'),
    path('registration/', views.CustomerRegistrationView.as_view(),
         name='customerregistration'),

    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),


    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='app/password_reset.html'),
         name='password_reset'),

    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),
         name='password_reset_done'),

    path('password_reset_confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html'), name='password_reset_confirm'),

    path('password_reset_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),
]
