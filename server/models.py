from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.validators import RegexValidator
from django.db.models.signals import post_save, post_delete

class Membre(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="membre")
    phone_regex=RegexValidator(regex=r'^(\+221)?[- ]?(77|70|76|78)[- ]?([0-9]{3})[- ]?([0-9]{2}[- ]?){2}$', message="le numero de telephone est invalide!")
    nom= models.CharField(max_length= 255)
    prenom= models.CharField(max_length= 255)
    online =models.BooleanField()
    telephone = models.CharField(validators=[phone_regex],max_length=20)
    niveau = models.CharField(max_length=100)
    nom_organisation = models.CharField(max_length=100)

    def __str__(self):
        return str(self.prenom + ' '+ self.nom )
    
    __repr__=__str__
    
class Admin(Membre):
    pass

class SuperAdmin(Membre):
    pass

class Anonyme(models.Model):
    username=models.CharField(max_length=50)
    def __str__(self): 
        return self.username

class Profile(models.Model):
    user=models.ForeignKey(Membre, on_delete=models.CASCADE,related_name="Profile")
    nombre_point = models.IntegerField()
    nombre_post = models.IntegerField()
    bio = models.CharField(max_length=500, null= True)
    photo = models.ImageField(null= True)

class Categorie(models.Model):
    titre =  models.CharField(max_length=50)
    admin=models.ManyToManyField(Admin)
    def __str__(self): 
        return self.titre

class Tag(models.Model):
    nom= models.CharField(max_length= 255)
    def __str__(self): 
        return self.nom

class Discussion(models.Model):
    user=models.ForeignKey(Membre, on_delete=models.CASCADE,related_name="Discussion")
    description=models.TextField()
    titre =  models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    resolue = models.BooleanField()
    tag= models.ForeignKey(Tag, on_delete= models.SET_NULL, null= True)
    nombre_post = models.IntegerField()
    def __str__(self): 
        return self.titre

class Post(models.Model):
    user=models.ForeignKey(Membre, on_delete=models.CASCADE,related_name="Post")
    body= models.TextField()
    heure_creation = models.DateTimeField(auto_now_add=True)
    modifie = models.BooleanField()
    likes_count = models.IntegerField(default=0)
    dislikes_count = models.IntegerField(default=0)
    modifie_date=models.DateTimeField(auto_now_add=True)
    utile = models.BooleanField()
    discussion=models.ForeignKey(Discussion, on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']

class Question(Post):
    question_id = models.AutoField

class Reponse(Post):
    response_id = models.AutoField
    point = models.ForeignKey(Question, on_delete=models.CASCADE, default='question_to_answer')
    
    def user_response_question(sender, instance, *args, **kwargs):
        response = instance
        post = response.point
        sender = response.user

        notify = Notification(post=post, sender=sender, recevier=post.user, notification_type=3)
        notify.save()
post_save.connect(Reponse.user_response_question, sender=Reponse)

class Rate(models.Model):
    like = models.BooleanField()
    dislike = models.BooleanField()
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    rate=models.ForeignKey(Membre, on_delete=models.DO_NOTHING)

class Signale(models.Model):
    membre=models.ForeignKey(Membre, on_delete=models.CASCADE,related_name="Signale")
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    
class Notification(models.Model):
    NOTIFICATION_TYPES = ((1, 'Like'),(2, 'Dislike'),(3,"Response"))

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='noti_post', blank=True, null=True)
    sender = models.ForeignKey(Membre, on_delete=models.CASCADE, related_name='noti_from_user')
    recevier = models.ForeignKey(Membre, on_delete=models.CASCADE, related_name='noti_to_user')
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPES)
    date = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)
    
class Message(models.Model):
    #user = models.ForeignKey(Membre, on_delete=models.CASCADE, related_name='msg_user')
    sender = models.ForeignKey(Membre, on_delete=models.CASCADE, related_name='from_user')
    recipient = models.ForeignKey(Membre, on_delete=models.CASCADE, related_name='to_user')
    body = models.TextField(max_length=1000, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    def send_message(from_user, to_user, body):
        sender_message = Message(
            sender=from_user,
            recipient=to_user,
            body=body,
            is_read=True)
        sender_message.save()

        
        return sender_message

    def get_messages(user):
        messages = Message.objects.filter(sender=user).values('recipient').annotate(last=Max('date')).order_by('-last')
        users = []
        for message in messages:
            users.append({
                'user': Membre.objects.get(pk=message['recipient']),
                'last': message['last'],
                'unread': Message.objects.filter(user=user, recipient__pk=message['recipient'], is_read=False).count()
            })
        return users

class Likes(models.Model):
    user = models.ForeignKey(Membre, on_delete=models.CASCADE, related_name='user_likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')
     
    def user_liked_post(sender, instance, *args, **kwargs):
        like = instance
        post = like.post
        sender = like.user
        #we got the sender and like from the like user that liking
        notify = Notification(post=post, sender=sender, recevier=post.user, notification_type=1)
        notify.save()
    def user_unlike_post(sender, instance, *args, **kwargs):
        like = instance
        post = like.post
        sender = like.user
        notify = Notification.objects.filter(post=post, sender=sender, notification_type=1)
        notify.delete()
post_save.connect(Likes.user_liked_post, sender=Likes)
post_save.connect(Likes.user_unlike_post, sender=Likes)
