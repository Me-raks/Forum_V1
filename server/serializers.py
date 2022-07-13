from rest_framework import serializers 
from django.shortcuts import get_object_or_404
from .models import *
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework.response import Response
from rest_framework import status


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','email','first_name','last_name','password']

        extra_kwargs = {
            'username': {'validators': []}
        }
    

class MembreSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model=Membre
        fields='__all__'

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

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user         
        instance.telephone = validated_data.get('telephone', instance.telephone)
        instance.niveau = validated_data.get('niveau', instance.niveau)
        instance.nom_organisation = validated_data.get('nom_organisation', instance.nom_organisation)
        instance.save()
        user.username = user_data.get('username', user.username)
        user.email = user_data.get('email', user.email)
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.password = user_data.get('password', user.password)
        user.save()
        return instance

        
class ModerateurSerializer(serializers.ModelSerializer):
    membre=MembreSerializer()

    class Meta:
        model=Moderateur
        fields=['id','membre']

    def create(self, validated_data):
        membre = validated_data.pop('membre')
        user= membre.pop('user')
        telephone=membre["telephone"]
        username=user["username"]
        password=user["password"]
        email=user["email"]
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
        membre=Membre.objects.create(user=user,**membre)
        moderateur=Moderateur.objects.create(membre=membre,**validated_data)
        content_type = ContentType.objects.get_for_model(Moderateur)
        permission = Permission.objects.filter(codename='is_moderateur').first()
        if permission:
            user.user_permissions.add(permission)
        else:
            created = Permission.objects.create(codename='is_moderateur', name='is moderateur', content_type=content_type)
            user.user_permissions.add(created)
        return moderateur

    def update(self, instance, validated_data,*args, **kwargs):    
        if 'membre' in validated_data.keys():   
            membre_data = validated_data.pop('membre')
            membre_serializer = MembreSerializer(data = membre_data,partial=True) 
            if membre_serializer.is_valid():
                membre = membre_serializer.update(instance=instance.membre, validated_data=membre_serializer.validated_data)

class AdminSerializer(serializers.ModelSerializer):
    membre=MembreSerializer()

    class Meta:
        model=Admin
        fields=['id','membre']

    def create(self, validated_data):
        membre = validated_data.pop('membre')
        user= membre.pop('user')
        telephone=membre["telephone"]
        username=user["username"]
        password=user["password"]
        email=user["email"]
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
        membre=Membre.objects.create(user=user,**membre)
        admin=Admin.objects.create(membre=membre,**validated_data)
        content_type = ContentType.objects.get_for_model(Moderateur)
        permission = Permission.objects.filter(codename='is_admin').first()
        if permission:
            user.user_permissions.add(permission)
        else:
            created = Permission.objects.create(codename='is_admin', name='is admin', content_type=content_type)
            user.user_permissions.add(created)
        return admin

    def update(self, instance, validated_data,*args, **kwargs):    
        if 'membre' in validated_data.keys():   
            membre_data = validated_data.pop('membre')
            membre_serializer = MembreSerializer(data = membre_data,partial=True) 
            if membre_serializer.is_valid():
                membre = membre_serializer.update(instance=instance.membre, validated_data=membre_serializer.validated_data)


class SuperAdminSerializer(serializers.ModelSerializer):
    membre=MembreSerializer()
    class Meta:
        model = Admin
        fields=['id','membre']

    def create(self, validated_data):
        membre = validated_data.pop('membre')
        user= membre.pop('user')
        telephone=membre["telephone"]
        username=user["username"]
        password=user["password"]
        email=user["email"]
        if Membre.objects.filter(telephone=telephone).exists():
            raise serializers.ValidationError('Ce membre existe déja')
            return telephone
        if User.objects.filter(email=email).exists() :
            raise serializers.ValidationError('Ce membre existe déja')
            return email
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Ce compte existe déja')
            return username
        user=Compte.objects.create_user(**user)
        membre=Membre.objects.create(compte=compte,**membre)
        super_admin= SuperAdmin.objects.create(membre=membre,**validated_data)
        content_type = ContentType.objects.get_for_model(SuperAdmin)
        permission = Permission.objects.filter(codename='is_super_admin').first()
        if permission:
            user.user_permissions.add(permission)
        else:
            created = Permission.objects.create(codename='is_super_admin', name='is super_admin', content_type=content_type)
            user.user_permissions.add(created)
        return super_admin

    def update(self, instance, validated_data,*args, **kwargs):    
        if 'membre' in validated_data.keys():   
            membre_data = validated_data.pop('membre')
            membre_serializer = MembreSerializer(data = membre_data,partial=True) 
            if membre_serializer.is_valid():
                membre = membre_serializer.update(instance=instance.membre, validated_data=membre_serializer.validated_data)


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields ='__all__'

    def create(self, validated_data):
        sender = validated_data.pop('sender')
        to_user_username = validated_data.get('recipient')
        body = validated_data.get('body')
        messages=Message.objects.create(sender=sender,**validated_data)
        return messages

    def update(self, instance, validated_data,*args, **kwargs):  
        if 'sender' in validated_data.keys():      
            instance.sender = validated_data.get('sender', instance.sender)
        if 'recipient' in validated_data.keys():
            instance.recipient= validated_data.get('recipient', instance.recipient)
        if 'body' in validated_data.keys():
            instance.body= validated_data.get('body', instance.body)
        instance.save()
        return instance


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields ='__all__'
class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model=Categorie
        fields ='__all__'
        
    def create(self, validated_data):
        created_By = validated_data.pop('created_By')
        titre=validated_data.get('titre')
        if Categorie.objects.filter(titre=titre).exists():
            raise serializers.ValidationError('Cette Categorie existe déja')
            return titre
        instance=Categorie.objects.create(titre=titre)
        instance.created_By.set(created_By)
        instance.save()
        return instance
    def update(self, instance, validated_data):
        instance.titre = validated_data.get('titre', instance.titre)
        instance.save()
        return instance

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields ='__all__'
    def create(self, validated_data):
        categorie=validated_data.get('categorie')
        created_By=validated_data.get('created_By')
        nom=validated_data.get('nom')
        if Tag.objects.filter(nom=nom).exists():
            raise serializers.ValidationError('Cette tag existe déja')
            return titre
        instance=Tag.objects.create(nom=nom,categorie=categorie)
        instance.created_By.set(created_By)
        instance.save()
        return instance
    def update(self, instance, validated_data):
        instance.titre = validated_data.get('titre', instance.titre)
        instance.save()
        return instance

class DiscussionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discussion
        fields ='__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields ='__all__'

    def create(self, validated_data):
        user= validated_data.pop('user')
        body=validated_data.get('body')
        discussion=validated_data.get('discussion')
        post=Post.objects.create(user=user,**validated_data)
        posted = get_object_or_404(Post, body=post)
        membre = Membre.objects.get(id = user.id)
        profile =  Profile.objects.get(membre=membre.id)
        profile.nombre_post+=1
        profile.save()
        return post
    def update(self, instance, validated_data):
        question = instance.question         
        instance.body = validated_data.get('body', instance.body)
        instance.discussion = validated_data.get('discussion', instance.discussion)
        instance.modifie = validated_data.get('modifie', instance.modifie)
        instance.modifie_date = validated_data.get('modifie_date', instance.modifie_date)
        instance.save()
        return instance
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields ='__all__'

    def create(self, validated_data):
        user= validated_data.pop('user')
        body=validated_data.get('body')
        discussion=validated_data.get('discussion')
        post=Post.objects.create(user=user,**validated_data)
        posted = get_object_or_404(Post, body=post)
        membre = Membre.objects.get(id = user.id)
        profile =  Profile.objects.get(membre=membre.id)
        profile.nombre_post+=1
        profile.save()
        return post
        
    def update(self, instance, validated_data):
        question = instance.question         
        instance.body = validated_data.get('body', instance.body)
        instance.discussion = validated_data.get('discussion', instance.discussion)
        instance.modifie = validated_data.get('modifie', instance.modifie)
        instance.modifie_date = validated_data.get('modifie_date', instance.modifie_date)
        instance.save()
        return instance

class ReponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reponse
        fields ='__all__'

        def create(self, validated_data):
            body=validated_data.get('body')
            discussion=validated_data.get('discussion')
            post_to_answer=validated_data.get(post)
            post=Post.objects.create(user=user,**validated_data)
            posted = get_object_or_404(Post, body=post)
            membre = Membre.objects.get(id = user.id)
            profile =  Profile.objects.get(membre=membre.id)
            profile.nombre_post+=1
            post.responses_count+=1
            post.save()
            profile.save()
            return post

        def update(self, instance, validated_data):
            reponse = instance.reponse         
            instance.body = validated_data.get('body', instance.body)
            instance.discussion = validated_data.get('discussion', instance.discussion)
            instance.modifie = validated_data.get('modifie', instance.modifie)
            instance.modifie_date = validated_data.get('modifie_date', instance.modifie_date)
            instance.post = validated_data.get('post', instance.post)
            instance.save()
            return instance


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = '__all__'

    def create(self ,validated_data ):
        post = validated_data.pop('post')
        user = validated_data.get('user')
        posted = get_object_or_404(Post, body=post)
        membre = Membre.objects.get(id = user.id)
        profile =  Profile.objects.get(membre=membre.id)
        if Likes.objects.filter(user=user,post=post).exists():
            posted.likes_count -=1
            profile.nombre_likes-=1
            profile.save()
            posted.save()
            Likes.objects.filter(user=user, post=post).delete()
        else:
            like=Likes.objects.create(user=user, post=post)
            posted.likes_count +=1
            profile.nombre_likes+=1
            profile.save()
            posted.save()
        return Historique.objects.create(user=user,post=post)

    

class DislikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dislikes
        fields = '__all__'

    def create(self ,validated_data ):
        post = validated_data.pop('post')
        user = validated_data.get('user')
        likes=Likes.objects.all()
        posted = get_object_or_404(Post, body=post)
        membre = Membre.objects.get(id = user.id)
        profile =  Profile.objects.get(membre=membre.id)
        if Dislikes.objects.filter(user=user, post=post).exists():
            posted.dislikes_count -=1
            profile.nombre_dislikes-=1
            profile.save()
            posted.save()
            Dislikes.objects.filter(user=user, post=post).delete()
        else:
            posted.dislikes_count +=1
            profile.nombre_dislikes+=1
            profile.save()
            posted.save()
            Dislikes.objects.create(user=user, post=post)
        return Historique.objects.create(user=user,post=post)
 
class SignaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signale
        fields = '__all__'

    def create(self ,validated_data ):
        post = validated_data.pop('post')
        user = validated_data.get('user')
        likes=Likes.objects.all()
        posted = get_object_or_404(Post, body=post)
        membre = Membre.objects.get(id = user.id)
        profile =  Profile.objects.get(membre=membre.id)
        if Signale.objects.filter(user=user, post=post).exists():
            posted.signale_count -=1
            profile.nombre_signale-=1
            profile.save()
            posted.save()
            Dislikes.objects.filter(user=user, post=post).delete()
            return Historique.objects.create(user=user,post=post)
        else:
            posted.signale_count +=1
            profile.nombre_signale+=1
            profile.save()
            posted.save()
            Signale.objects.create(user=user, post=post)
        return Historique.objects.create(user=user,post=post)

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(
        max_length=255, min_length=3, read_only=True)

    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        filtered_user_by_email = User.objects.filter(email=email)
        user = auth.authenticate(email=email, password=password)

        if filtered_user_by_email.exists() and filtered_user_by_email[0].auth_provider != 'email':
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }

        return super().validate(attrs)
