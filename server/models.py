import uuid
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.validators import RegexValidator
from django.db.models.signals import post_save, post_delete

class Membre(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="membre")
    phone_regex=RegexValidator(regex=r'^(\+221)?[- ]?(77|70|76|78)[- ]?([0-9]{3})[- ]?([0-9]{2}[- ]?){2}$', message="le numero de telephone est invalide!")
    is_online =models.BooleanField()
    telephone = models.CharField(validators=[phone_regex],max_length=20)
    niveau = models.CharField(max_length=100)
    nom_organisation = models.CharField(max_length=100)

    def __str__(self):
        return str(self.user.username)
    __repr__=__str__
    

class Moderateur(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    membre = models.ForeignKey(Membre, related_name = "Moderateur", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.membre.user.first_name + ' ' +self.membre.user.last_name)

    __repr__=__str__


class Admin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    membre = models.ForeignKey(Membre, related_name = "Admin", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.membre.user.first_name + ' ' +self.membre.user.last_name)

    __repr__=__str__


class SuperAdmin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    membre=models.ForeignKey(Membre,related_name="Super_Admin", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.membre.user.first_name + ' ' +self.membre.user.last_name)

    __repr__=__str__


class Anonyme(models.Model):
    username=models.CharField(max_length=50)
    def __str__(self): 
        return self.username


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    membre=models.ForeignKey(Membre, on_delete=models.CASCADE,related_name="Profile")
    nombre_likes = models.IntegerField(default=0)
    nombre_dislikes = models.IntegerField(default=0)
    nombre_signale = models.IntegerField(default=0)
    nombre_post = models.IntegerField(default=0)
    bio = models.CharField(max_length=500, null= True)
    photo = models.ImageField(null= True)
    
    def __str__(self):
        return str(self.membre.user.first_name + ' ' +self.membre.user.first_name)

    __repr__=__str__


class Categorie(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titre = models.CharField(max_length=100)
    created_By = models.ManyToManyField(Admin)
    def __str__(self):
        return str(self.titre)

    __repr__=__str__


class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom= models.CharField(max_length= 255)
    categorie=models.ForeignKey(Categorie, on_delete=models.CASCADE,related_name="Categorie")
    created_By = models.ManyToManyField(Membre)

    def __str__(self): 
        return self.nom

    __repr__=__str__
    

class Discussion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    membre=models.ForeignKey(Membre, on_delete=models.CASCADE,related_name="Discussion")
    description=models.TextField()
    titre =  models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    resolue = models.BooleanField()
    tag= models.ForeignKey(Tag, on_delete= models.SET_NULL, null= True)
    nombre_post = models.IntegerField(default=0)
    

    def __str__(self): 
        return self.titre

    __repr__=__str__


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    responses_count = models.IntegerField(default=0)
    user=models.ForeignKey(Membre, on_delete=models.CASCADE,related_name="Post")
    body= models.TextField()
    posted = models.DateTimeField(auto_now_add=True)
    modifie = models.BooleanField()
    likes_count = models.IntegerField(default=0)
    dislikes_count = models.IntegerField(default=0)
    signale_count = models.IntegerField(default=0)
    modifie_date=models.DateTimeField(auto_now_add=True)
    utile = models.BooleanField()
    discussion=models.ForeignKey(Discussion, on_delete=models.CASCADE)
    def __str__(self): 
        return str(self.body)

    __repr__=__str__


class Question(Post):
    def __str__(self): 
        return str(self.body)


class Reponse(Post):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    
    def user_response_post(sender, instance, *args, **kwargs):
        reponse = instance
        post = reponse.post
        sender = reponse.user
        text_preview = reponse.body[:50]
        notify = Notification(post=post, sender=sender, recevier=post.user, text_preview=text_preview, notification_type=3)
        notify.save()

    def user_del_response_post(sender, instance, *args, **kwargs):
        reponse = instance
        post = reponse.post
        sender = reponse.user
        notify = Notification.objects.filter(post=post, sender=sender, notification_type=3)
        notify.delete()

    def __str__(self): 
        return self.post.body

    __repr__=__str__



class Historique(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user=models.ForeignKey(Membre, on_delete=models.CASCADE,related_name="user_action")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_historique')
    is_liked=models.BooleanField(default=False)
    is_disliked=models.BooleanField(default=False)
    is_signale=models.BooleanField(default=False)

    def __str__(self): 
        return str(self.post)

    __repr__=__str__


class Notification(models.Model):
    NOTIFICATION_TYPES = ((1, 'Like'),(2, 'Dislike'),(3,"Response"),(4,"Signale"),(5,"Add a Tag"),(6,"Anonyne's Post"))
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='noti_post', blank=True, null=True)
    sender = models.ForeignKey(Membre, on_delete=models.CASCADE, related_name='noti_from_user')
    recevier = models.ForeignKey(Membre, on_delete=models.CASCADE, related_name='noti_to_user')
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPES)
    text_preview=models.CharField(max_length=50,blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return str(self.sender.user.username +self.recevier.user.username )
    __repr__=__str__

    
class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(Membre, on_delete=models.CASCADE, related_name='from_user')
    recipient = models.ForeignKey(Membre, on_delete=models.CASCADE, related_name='to_user')
    body = models.TextField(max_length=1000, blank=True, null=True)
    date_send = models.DateTimeField(auto_now_add=True)
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
        messages = Message.objects.filter(sender=sender).values('recipient').annotate(last=Max('date')).order_by('-last')
        users = []
        for message in messages:
            users.append({
                'user': User.objects.get(pk=message['recipient']),
                'last': message['last'],
                'unread': Message.objects.filter(user=user, recipient__pk=message['recipient'], is_read=False).count()
            })
        return users

    def __str__(self): 
        return str(self.sender.user.username + ' ' +self.recipient.user.username)

    __repr__=__str__


class Signale(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Membre, on_delete=models.CASCADE, related_name='user_signale')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_signale')

    def user_signale_post(instance,*args, **kwargs):
        like=instance
        post=like.post
        sender = like.user
        notify = Notification(post=post, sender=sender, recevier=post.user, notification_type=4)
        notify.save()

    def user_unsignale_post(sender, instance, *args, **kwargs):
        like = instance
        post = like.post
        sender = like.user
        notify = Notification.objects.filter(post=post, sender=sender, notification_type=4)
        notify.delete()
    def __str__(self):
        return str(self.post.body)

    __repr__=__str__


class Likes(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Membre, on_delete=models.CASCADE, related_name='user_likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')

    def user_liked_post(instance,*args, **kwargs):
        like=instance
        post=like.post
        sender = like.user
        notify = Notification(post=post, sender=sender, recevier=post.user, notification_type=1)
        notify.save()

    def user_unlike_post(sender, instance, *args, **kwargs):
        like = instance
        post = like.post
        sender = like.user
        notify = Notification.objects.filter(post=post, sender=sender, notification_type=1)
        notify.delete()
    def __str__(self):
        return str(self.post.body)

    __repr__=__str__


class Dislikes(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Membre, on_delete=models.CASCADE, related_name='user_dislikes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_dislikes')

    def user_disliked_post(instance,*args, **kwargs):
        like=instance
        post=like.post
        sender = like.user
        notify = Notification(post=post, sender=sender, recevier=post.user, notification_type=2)
        notify.save()

    def user_undislike_post(sender, instance, *args, **kwargs):
        like = instance
        post = like.post
        sender = like.user
        notify = Notification.objects.filter(post=post, sender=sender, notification_type=2)
        notify.delete()
    def __str__(self):
        return str(self.post.body)

    __repr__=__str__


post_save.connect(Dislikes.user_disliked_post, sender=Dislikes)
post_delete.connect(Dislikes.user_undislike_post, sender=Dislikes)
post_save.connect(Likes.user_liked_post, sender=Likes)
post_delete.connect(Likes.user_unlike_post, sender=Likes)
post_save.connect(Signale.user_signale_post, sender=Signale)
post_delete.connect(Signale.user_unsignale_post, sender=Signale)
post_save.connect(Reponse.user_response_post, sender=Reponse)
post_delete.connect(Reponse.user_del_response_post, sender=Reponse)