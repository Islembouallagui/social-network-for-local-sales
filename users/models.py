from django.db import models
from django.contrib.auth.models import User,AbstractUser
from PIL import Image
from django.utils import timezone
from django.db.models import Max
#from blog.models import Post
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.gis.db import models
from django.contrib.gis.gdal import OGRGeometry
from django.contrib.gis import forms
from django.contrib.gis.geos import Point
from django.core.validators import MaxValueValidator, MinValueValidator



class User(AbstractUser):
    Latitude = models.FloatField(default=0.000,null=True)
    Longitude = models.FloatField(default=0.000,null=True)
    geo_location = models.PointField(geography=True, default=Point(0.0, 0.0))
    class Meta:
        db_table = 'auth_user'





class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    image = models.ImageField(default='default - Copie.jpg', upload_to='profile_pics')
    phone = models.IntegerField(default=0)
    
    #post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)




class Service(models.Model):
    userr = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    email_business=models.EmailField()
    phone_business = models.IntegerField()
    name_business = models.CharField(max_length=200)
    sector = models.CharField(max_length=200)
    description = models.CharField(max_length=5000, default="")
    #principal_image = models.FileField(blank=True,upload_to = 'images/')
    location = models.PointField(null=True,default=Point(0.0,0.0))
    disponibilite = models.CharField(max_length=5000, default="")
    Latitude = models.FloatField(default=0.000,null=True)
    Longitude = models.FloatField(default=0.000,null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    Adress = models.CharField(max_length=200,default="")
    image_service = models.ImageField(default='default - Copie.jpg', upload_to='profile_pics')

    
    def __str__(self):
       return str(self.name_business)    

RATE_CHOICES = [
    (1, '1 - Trash'),
    (2, '2 - Horrible'),
    (3, '3 - Terrible'),
    (4, '4 - Bad'),
    (5, '5 - OK'),
    (6, '6 - acceptable'),
    (7, '7 - Good'),
    (8, '8 - Very Good'),
    (9, '9 - Perfect'),
    (10, '10 - More than perfect'), 
]


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=3000, blank=True)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES)
   

    def __str__(self):
        return self.user.username 



class Prod(models.Model):
    userr = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    Shop = models.CharField(max_length=200,default="")
    Adress = models.CharField(max_length=200,default="")
    description = models.CharField(max_length=5000, default="")
    disponibilite = models.BooleanField(default=True)
    prix = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    Title = models.CharField(max_length=5000, default="")
    quantité = models.CharField(max_length=1000, default="")
    date_posted = models.DateTimeField(default=timezone.now)
    principal_image = models.FileField(blank=True)
    location = models.PointField(null=True,default=Point(0.0,0.0))
    Latitude = models.FloatField(default=0.000,null=True)
    Longitude = models.FloatField(default=0.000,null=True)
    
    def __str__(self):
       return str(self.Title)

class ProdImage(models.Model):
    prod = models.ForeignKey(Prod, default=None, on_delete=models.CASCADE)
    image = models.FileField(upload_to = 'images/')

    def __str__(self):
        return self.prod.Title
class Message(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user')
    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='from_user')
    recipient = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='to_user')
    body = models.TextField(max_length=1000, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    def send_message(from_user, to_user, body):
        sender_message = Message(
            user=from_user,
            sender=from_user,
            recipient=to_user,
            body=body,
            is_read=True)
        sender_message.save()
        recipient_message = Message(
            user=to_user,
            sender=from_user,
            body=body,
            recipient=from_user,)
        recipient_message.save()
        return sender_message
    def get_messages(user):
        messages = Message.objects.filter(user=user).values('recipient').annotate(last=Max('date')).order_by('-last')
        users = []
        for message in messages:
            users.append({
                'user': User.objects.get(pk=message['recipient']),
                'last': message['last'],
                'unread': Message.objects.filter(user=user, recipient__pk=message['recipient'], is_read=False).count()
                })
        return users









   

 