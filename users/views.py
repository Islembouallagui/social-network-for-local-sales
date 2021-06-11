from django.shortcuts import render, redirect,HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm,addproduct,ServiceRegisterForm
from .models import *
#from .forms import updateprod
from django.contrib.auth.models import User
from django.template import loader
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (

    UpdateView,
    DeleteView,
    )
from django.template import loader, RequestContext
from django.http import HttpResponse,HttpResponseBadRequest
from django.db.models import Q
from django.core.paginator import Paginator
from blog.views import *
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import fromstr
from django.contrib.gis.measure import D
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django.contrib.gis.db.models.functions import Distance
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import Context, Template, RequestContext
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.views.generic import ListView, DetailView, View
from .forms import RateForm
from django.db.models import Avg
from .models import Review
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render, redirect


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            email = form.cleaned_data['email']
            upass = form.cleaned_data['password1']
            Longitude =float(request.POST.get('longitude'))
            Latitude = float(request.POST.get('latitude'))
            user = get_user_model()
            
            #user.is_active = False
            user = user.objects.create_user(username, email,upass)
            user.last_name = lastname
            user.first_name = firstname
            user.Latitude = request.POST.get('latitude')
            user.Longitude = request.POST.get('longitude')
            user.geo_location = Point(Latitude,Longitude)
            #user.is_active = False
            user.save()
            #current_site = get_current_site(request)
            #mail_subject = 'Activate your blog account.'
            
            #message = render_to_string('acc_active_email.html',context)
            #{
                #'user': user,
                #'domain': current_site.domain,
                #'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                #'token':account_activation_token.make_token(user),
            #})
            #to_email = form.cleaned_data.get('email')
            #email = EmailMessage(
                        #mail_subject, message, to=[to_email]
            #)
            #email.send()
            
            messages.success(request, f'Your account has been created you are now able to logIn')
            return redirect('login')
           
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

@login_required
def profile(request):
    user = get_user_model()
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    
    userx = request.user
    services = Service.objects.filter(userr_id=userx.id)
    prods = Prod.objects.filter(userr_id=userx.id)
    posts = Post.objects.filter(author_id=userx.id)
    return render(request, 'users/profile.html',{'u_form':u_form,'p_form':p_form,'prods':prods,'posts':posts,'services':services})#add detail page


def productdetail(request):
  idprod = request.GET.get('id')
  prods = Prod.objects.get(id=idprod)
  photos = ProdImage.objects.filter(prod_id=idprod)
  return render(request,'users/productdetail.html',{'prods':prods,'photos':photos})


def add_service(request):

      if request.method == 'POST':
         formservice = ServiceRegisterForm(request.POST,request.FILES)
         images = request.FILES.getlist('images')
         if formservice.is_valid():
      
            email_business = formservice.cleaned_data.get('email_business')
            phone_business =  formservice.cleaned_data.get('phone_business')
            name_business =  formservice.cleaned_data.get('name_business')
            sector = formservice.cleaned_data.get('sector')
            disponibilite=formservice.cleaned_data.get('disponibilite')
            description = formservice.cleaned_data.get('description')
            Adress = formservice.cleaned_data.get('Adress')
            image_service = formservice.cleaned_data.get('image_service')
            #principal_image=formservice.cleaned_data.get('principal_image')
            Longitude =float(request.POST.get('longitude'))
            Latitude = float(request.POST.get('latitude'))
            
            service = Service()
            service.userr = request.user
            service.email_business = email_business
            service.phone_business = phone_business
            service.name_business = name_business
            service.sector = sector
            service.Adress = Adress
            service.description= description            
            service.disponibilite= disponibilite
            service.image_service= image_service
            #service.principal_image = principal_image
            service.Latitude = request.POST.get('latitude')
            service.Longitude = request.POST.get('longitude')
            service.location = Point(Latitude,Longitude)
            service.save()
            

         return redirect('profile')
      else:
        formservice = ServiceRegisterForm()
      userr = request.user
      return render(request,'users/serviceForm.html',{'formservice':formservice})
def updateService(request, pk):
  services = Service.objects.get(id=pk)
  form = ServiceRegisterForm(instance=services)

  if request.method == 'POST':
    form = ServiceRegisterForm(request.POST, instance=services)
    if form.is_valid():
       form.save()
       return redirect('services')

  context = {'form':form}
  return render(request, 'users/service_form.html', context)

def deleteService(request, pk):
  services = Service.objects.get(id=pk)
  if request.method == "POST":
    services.delete()
    return redirect('services')

  context = {'item':services}
  return render(request, 'users/service_confirm_delete.html', context)



def Rate(request, pk):
  service = Service.objects.get(id=pk)
  user = request.user
  if request.method == 'POST':
    form = RateForm(request.POST)
    if form.is_valid():
      rate = form.save(commit=False)
      rate.user = user
      rate.service = service
      rate.save()
      return redirect('services')
 # return HttpResponseRedirect(reverse('service-details', args=[idservice]))
  else:
    form = RateForm()

  #template = loader.get_template('rate.html')

  context = {
    'form': form, 
    'service': service,
  }
#return HttpResponse(template.render(context, request))
  return render(request, 'users/rate.html', context)
def servicedetail(request):
  idservice = request.GET.get('id')
  services = Service.objects.get(id=idservice)
  reviews = Review.objects.filter(service_id=services)
  reviews_avg = reviews.aggregate(Avg('rate'))
  reviews_count = reviews.count()
  our_db = True
  context={
  'services':services,
  'reviews': reviews,
  'reviews_avg': reviews_avg,
  'reviews_count': reviews_count,
  'our_db': our_db,

  }
  return render(request,'users/servicedetail.html',context)
@login_required
def add_product(request):
    if request.method == "POST":
        productform = addproduct(request.POST,request.FILES)
        images = request.FILES.getlist('images')

        if productform.is_valid():
            Title = productform.cleaned_data.get('Title')           
            prix = productform.cleaned_data.get('prix')
            description =  productform.cleaned_data.get('description')
            disponibilite =  productform.cleaned_data.get('disponibilite')
            quantité = productform.cleaned_data.get('quantité')
            principal_image = productform.cleaned_data.get('principal_image') 
            Shop = productform.cleaned_data.get('Shop')
            Adress = productform.cleaned_data.get('Adress')
            Longitude =float(request.POST.get('longitude'))
            Latitude = float(request.POST.get('latitude'))
            prod = Prod() 
            prod.userr = request.user
            prod.Title= Title
            prod.prix = prix
            prod.description= description            
            prod.disponibilite= disponibilite
            prod.quantité = quantité
            prod.principal_image = principal_image
            prod.Latitude = request.POST.get('latitude')
            prod.Longitude = request.POST.get('longitude')
            prod.location = Point(Latitude,Longitude)
            prod.Shop = Shop
            prod.Adress = Adress
            prod.save()
            for image in images:

               prodImage = ProdImage.objects.create(
               prod = prod,
               image = image)
            
            
            return redirect('profile')
    else:
        productform = addproduct()
    userr = request.user
    return render(request, 'users/add_product.html', {'productform': productform })

def updateOrder(request, pk):
  prods = Prod.objects.get(id=pk)
  form = addproduct(instance=prods)

  if request.method == 'POST':
    form = addproduct(request.POST, instance=prods)
    if form.is_valid():
       form.save()
       return redirect('products')

  context = {'form':form}
  return render(request, 'users/prod_form.html', context)

def deleteOrder(request, pk):
  prods = Prod.objects.get(id=pk)
  if request.method == "POST":
    prods.delete()
    return redirect('products')

  context = {'item':prods}
  return render(request, 'users/prod_confirm_delete.html', context)





@login_required
def products(request):  
  current_user = request.user
  context ={
      'prods':Prod.objects.filter(location__distance_lte=(GEOSGeometry(current_user.geo_location),D(km=1000))),
       
       }
  queryset = Prod.objects.annotate(distance=Distance('location',
    GEOSGeometry(current_user.geo_location))
    ) 
  return render(request,'users/products.html',context)
#class ProdListView(ListView):
    #model = Prod
    #template_name = 'users/products.html '
    #context_object_name = 'prods'
    #geom = fromstr('POINT(-71 19)',srid=4326)
    #geo = Prod.objects.filter(location__dwithin=(geom, D(km=7)))
    #paginate_by = 6

@login_required
def services(request):
  current_user = request.user
  #paginate_by = 5
  context ={
       'services':Service.objects.filter(location__distance_lte=(GEOSGeometry(current_user.geo_location),D(km=1000))),
       }
  return render(request,'users/services.html',context)
#class ServiceListView(ListView):
    #model = Service
    #template_name = 'users/services.html '
    #context_object_name = 'services'
    #paginate_by = 6




# Create your views here.
@login_required
def Inbox(request):
  user = get_user_model()
  messages = Message.get_messages(user=request.user)
  active_direct = None
  directs = None

  if messages:
    message = messages[0]
    active_direct = message['user'].username
    directs = Message.objects.filter(user=request.user, recipient=message['user'])
    directs.update(is_read=True)
    for message in messages:
      if message['user'].username == active_direct:
        message['unread'] = 0

  context = {
    'directs': directs,
    'messages': messages,
    'active_direct': active_direct,
    }

  template = loader.get_template('users/direct.html')

  return HttpResponse(template.render(context, request))

@login_required
def UserSearch(request):
  query = request.GET.get("q")
  context = {}
  
  if query:
    users = get_user_model().objects.filter(Q(username__icontains=query))

    #Pagination
    paginator = Paginator(users, 6)
    page_number = request.GET.get('page')
    users_paginator = paginator.get_page(page_number)

    context = {
        'users': users_paginator,
      }
  
  template = loader.get_template('users/search_user.html')
  
  return HttpResponse(template.render(context, request))

@login_required
def Directs(request, username):
  user = request.user
  messages = Message.get_messages(user=user)
  active_direct = username
  directs = Message.objects.filter(user=user, recipient__username=username)
  directs.update(is_read=True)
  for message in messages:
    if message['user'].username == username:
      message['unread'] = 0

  context = {
    'directs': directs,
    'messages': messages,
    'active_direct':active_direct,
  }

  template = loader.get_template('users/direct.html')

  return HttpResponse(template.render(context, request))


@login_required
def NewConversation(request, username):
  from_user = request.user
  body = ''
  try:
    to_user = get_user_model().objects.get(username=username)
  except Exception as e:
    return redirect('usersearch')
  if from_user != to_user:
    Message.send_message(from_user, to_user, body)
  return redirect('inbox')

@login_required
def SendDirect(request):
  from_user = request.user
  to_user_username = request.POST.get('to_user')
  body = request.POST.get('body')
  
  if request.method == 'POST':
    to_user = get_user_model().objects.get(username=to_user_username)
    Message.send_message(from_user, to_user, body)
    return redirect('inbox')
  else:
    HttpResponseBadRequest()

def checkDirects(request):
  directs_count = 0
  if request.user.is_authenticated:
    directs_count = Message.objects.filter(user=request.user, is_read=False).count()

  return {'directs_count':directs_count}
@login_required
def ProductSearch(request):
  query = request.GET.get("q")
  context = {}
  
  if query:
    prods = Prod.objects.filter(Q(Title__icontains=query))

    #Pagination
    paginator = Paginator(prods, 6)
    page_number = request.GET.get('page')
    prods_paginator = paginator.get_page(page_number)

    context = {
        'prods': prods_paginator,
      }
  
  template = loader.get_template('users/search_prod.html')
  
  return HttpResponse(template.render(context, request))
@login_required
def ServiceSearch(request):
  query = request.GET.get("q")
  context = {}
  
  if query:
    services = Service.objects.filter(Q(name_business__icontains=query))

    #Pagination
    paginator = Paginator(services, 6)
    page_number = request.GET.get('page')
    services_paginator = paginator.get_page(page_number)

    context = {
        'services': services_paginator,
      }
  
  template = loader.get_template('users/search_service.html')
  
  return HttpResponse(template.render(context, request))

@login_required
def PostSearch(request):
  query = request.GET.get("q")
  context = {}
  
  if query:
    posts = Post.objects.filter(Q(title__icontains=query))

    #Pagination
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    posts_paginator = paginator.get_page(page_number)

    context = {
        'posts': posts_paginator,
      }
  
  template = loader.get_template('users/search_post.html')
  
  return HttpResponse(template.render(context, request))


def search_venues(request):
  if request.method =="POST":
      searched = request.POST['searched']
      prods = Prod.objects.filter(Title__contains=searched)
      posts = Post.objects.filter(title__contains=searched)
      services = Service.objects.filter(name_business__contains=searched)
      users = get_user_model().objects.filter(username__contains=searched)
      context = {
        'searched':searched,
        'prods':prods,
        'posts':posts,
        'services':services,
        'users':users
      }
      return render(request,'users/search_venues.html',context)
  else:
      return render(request,'users/search_venues.html')