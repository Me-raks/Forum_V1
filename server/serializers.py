from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'email']
        extra_kwargs = {
            'username': {'validators': []}
        }

class AdminSerializer(serializers.HyperlinkedModelSerializer):
    user=UserSerializer(many=False, read_only=True)
    class Meta:
        model = Admin
        fields = ['user']

class MembreSerializer(serializers.HyperlinkedModelSerializer):
    user=UserSerializer()
    class Meta:
        model = Membre
        fields = ['user','nom', 'prenom','telephone', 'niveau','nom_organisation']

        extra_kwargs = {
            'telephone': {'validators': []}
        }
    def create(self, validated_data):

        user = validated_data.pop('user')
        telephone=validated_data.get('telephone')
        username=validated_data.get('username')
        if Membre.objects.filter(telephone=telephone).exists():
            raise serializers.ValidationError('Ce membre existe déja')
            return telephone
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Ce compte existe déja')
            return user

        user=User.objects.create(**user)
        membre=Membre.objects.create(user=user,**validated_data)
        return membre
    def update(self, instance, validated_data):

        user_data = validated_data.pop('user')
        user = instance.user         
        instance.nom = validated_data.get('nom', instance.nom)
        instance.prenom = validated_data.get('prenom', instance.prenom)
        instance.telephone = validated_data.get('telephone', instance.telephone)
        instance.save()
        user.identifiant = user_data.get('username', user.username)
        user.email = user_data.get('email', user.email)
        user.password = user_data.get('password', user.password)
        user.save()
        
        return instance

class CategorieSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Categorie
        fields ='__all__'
    def create(self, validated_data):
        user = validated_data.pop('user')
        telephone=validated_data.get('titre')
        admin=Admin.objects.all()
        if Categorie.objects.filter(titre=titre).exists():
            raise serializers.ValidationError('Cette Categorie existe déja')
            return titre
        categorie=Categorie.objects.create(titre=titre,admin=admin)
        return categorie
class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"

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
        fields = '__all__'
    """def update(self,instance, validated_data):
        post_data = validated_data.pop('post')
        post = instance.post         
        instance.likes = validated_data.get('likes_count', instance.likes_count)
        #post_data = validated_data.pop('post')
        #post = instance.user
        #post_id = validated_data.get('id')
        post = get_object_or_404(Post, id=id)
        paginator = Paginator(profile_list, 25)
        print(1,post)
        current_likes = post.likes_count
        liked = Likes.objects.filter(user=user, post=post).count()
        if not liked:
            like = Likes.objects.create(user=user, post=post)
            current_likes +=  1
        else:
            Likes.objects.filter(user=user, post=post).delete()
            current_likes = current_likes - 1
        instance.likes_count = current_likes
        instance.save()
        return instance
    """
