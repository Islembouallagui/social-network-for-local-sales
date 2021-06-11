from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path,include
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import url



urlpatterns = [
    path('admin/', admin.site.urls),
    path('search_venues', user_views.search_venues, name='search-venues'),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('products/', user_views.products, name='products'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('productdetail/', user_views.productdetail, name='productdetail'),
    path('servicedetail/', user_views.servicedetail, name='servicedetail'),
    path('add_product/', user_views.add_product, name='add_product'),
    path('add_service/', user_views.add_service, name='add_service'),
    #path('products/',ProdListView.as_view(),name='products'),
    path('services/', user_views.services,name='services'),
    #path('productdetail/<int:pk>/<token>/update', user_views.ProdUpdateView.as_view(), name='prod-update'),
    #path('productdetail/<int:pk>/delete/', user_views.ProdDeleteView.as_view(), name='prod-delete'),
    path('update_prod/<str:pk>/', user_views.updateOrder, name="update_order"),
    path('delete_prod/<str:pk>/', user_views.deleteOrder, name="delete_order"),
    path('update_service/<str:pk>/', user_views.updateService, name="update_service"),
    path('delete_service/<str:pk>/', user_views.deleteService, name="delete_service"),
    path('rate/<str:pk>/',user_views.Rate, name="rate-service"),
   
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='users/password_reset.html'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'
         ),
         name='password_reset_complete'),

    path('', include('blog.urls')),
   

  
    path('search/', user_views.ProductSearch, name='prodsearch'),
    path('searchservice/', user_views.ServiceSearch, name='servicesearch'),
    path('searchprod/', user_views.PostSearch, name='postsearch'),
    #path('activate/(?P<uidb64>[0-9A-Za-z]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        #user_views.activate, name='activate'),
    #url(r'^$', user_views.home, name='home'),
    #url(r'^signup/$', user_views.register, name='register'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        user_views.activate, name='activate'),
   
    path('Inbox/', user_views.Inbox, name='inbox'),
    path('directs/<username>', user_views.Directs, name='directs'),
    path('new/', user_views.UserSearch, name='usersearch'),
    path('new/<username>',  user_views.NewConversation, name='newconversation'),
    path('send/', user_views.SendDirect, name='send_direct'),

]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)