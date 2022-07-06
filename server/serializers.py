from rest_framework import serializers 
from .models import *
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework.exceptions import AuthenticationFailed
import os



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','email','first_name','last_name','password']

        extra_kwargs = {
            'username': {'validators': []}
        }

class AdminSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model = Admin
        fields=['user','telephone','niveau','nom_organisation']

    def create(self, validated_data):

        user = validated_data.pop('user')
        telephone=validated_data.get('telephone')
        username=validated_data.get('username')
        email=validated_data.get('email')
        if Admin.objects.filter(telephone=telephone).exists():
            raise serializers.ValidationError('Ce membre existe déja')
            return telephone
        if User.objects.filter(email=email).exists() :
            raise serializers.ValidationError('Ce membre existe déja')
            return email
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Ce compte existe déja')
            return username
        user=User.objects.create_user(**user)
        admin=Admin.objects.create(user=user,**validated_data)
        content_type = ContentType.objects.get_for_model(Admin)
        permission = Permission.objects.filter(codename='is_admin').first()
        if permission:
            user.user_permissions.add(permission)
        else:
            created = Permission.objects.create(codename='is_admin', name='is admin', content_type=content_type)
            user.user_permissions.add(created)
        return admin


    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user         
        instance.telephone = validated_data.get('telephone', instance.telephone)
        instance.save()
        user.username = compte_data.get('username', user.username)
        user.email = compte_data.get('email', user.email)
        user.first_name = compte_data.get('first_name', user.first_name)
        user.last_name = compte_data.get('last_name', user.last_name)
        user.password = compte_data.get('password', user.password)
        user.save()
        return instancess


class MembreSerializer(serializers.ModelSerializer):
    user =UserSerializer()

    class Meta:
        model=Membre
        fields=['user','telephone','niveau','nom_organisation']

    def create(self, validated_data):
        user = validated_data.pop('user')
        telephone=validated_data.get('telephone')
        username=validated_data.get('username')
        email=validated_data.get('email')
        if Membre.objects.filter(telephone=telephone).exists():
            raise serializers.ValidationError('Ce membre existe déja')
            return telephone
        if User.objects.filter(email=email).exists() :
            raise serializers.ValidationError('Ce membre existe déja')
            return email
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Ce compte existe déja')
            return username

        user=User.objects.create_user(**user)
        membre=Membre.objects.create(user=user,**validated_data)
        return membre
    
    def update(self, instance, validated_data,*args, **kwargs):  
        if 'user' in validated_data.keys():   
            membre_data = validated_data.pop('user')
            membre_serializer = UserSerializer(data = membre_data,partial=True) 
            if membre_serializer.is_valid():
                membre = membre_serializer.update(instance=instance.membre, validated_data=membre_serializer.validated_data)
        if 'niveau' in validated_data.keys():   
            instance.niveau = validated_data.get('niveau', instance.niveau)
        if 'nom_organisation' in validated_data.keys():   
            instance.nom_organisation = validated_data.get('nom_organisation', instance.nom_organisation)
        instance.save()
        return instance

class ModerateurSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model=Moderateur
        fields=['user','telephone','niveau','nom_organisation']

    def create(self, validated_data):
        user = validated_data.pop('user')
        telephone=validated_data.get('telephone')
        username=validated_data.get('username')
        email=validated_data.get('email')
        if Moderateur.objects.filter(telephone=telephone).exists():
            raise serializers.ValidationError('Ce membre existe déja')
            return telephone
        if User.objects.filter(email=email).exists() :
            raise serializers.ValidationError('Ce membre existe déja')
            return email
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Ce compte existe déja')
            return username
        user=User.objects.create_user(**user)
        moderateur=Moderateur.objects.create(user=user,**validated_data)
        content_type = ContentType.objects.get_for_model(Moderateur)
        permission = Permission.objects.filter(codename='is_moderateur').first()
        if permission:
            user.user_permissions.add(permission)
        else:
            created = Permission.objects.create(codename='is_moderateur', name='is moderateur', content_type=content_type)
            user.user_permissions.add(created)
        return moderateur

class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = ['sender','recipient']
    def create(self, validated_data):
        user = validated_data.pop('user')
        sender = validated_data.get('sender')
        to_user_username = validated_data.get('recipient')
        body = validated_data.get('body')
        to_user = get_object_or_404(Membre, user=to_user_username)
        Message.send_message(sender, to_user, body)
        messages=Message.objects.create(user=user,**validated_data)
        return messages

class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model=Categorie
        fields='__all__'

class TagSerializer(serializers.HyperlinkedModelSerializer):
    categorie=CategorieSerializer()
    class Meta:
        model = Tag
        fields = ['url','nom','categorie']

class DiscussionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Discussion
        fields = "__all__"

class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"

class ReponseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Reponse
        fields = "__all__"

class NotificationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"

class PostSerializerone(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ['likes_count','user']
class LikesSerializer(serializers.HyperlinkedModelSerializer):
    #post=PostSerializerone()
    class Meta:
        model = Likes
        fields = ['posts','user']