from django.contrib.auth.models import User
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect
from rest_framework import viewsets
from rest_framework import permissions
from .models import *
from .serializers import *
from rest_framework.viewsets import ModelViewSet
from .permissions import *
from rest_framework.response import Response
from rest_framework import status


class UserViewSet(viewsets.ModelViewSet):
    serializer_class= UserSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [IsUtilisateurAuthenticated | IsModerateurAuthenticated | IsAdminAututhenticated | IsSuperAdminAututhenticated]
        elif self.request.method == "POST":
            self.permission_classes = [IsModerateurAuthenticated | IsAdminAututhenticated | IsSuperAdminAututhenticated]
        elif self.request.method == "PUT" or self.request.method == "PATCH":
            self.permission_classes = [IsUtilisateurAuthenticated | IsModerateurAuthenticated | IsAdminAututhenticated | IsSuperAdminAututhenticated]
        elif self.request.method=="DELETE":
            self.permission_classes = [IsAdminAututhenticated | IsSuperAdminAututhenticated]
        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        queryset= User.objects.all()
        user_id = self.request.GET.get('id_user')
        if user_id is not None:
            queryset = queryset.filter(id=user_id)
        return queryset


class MembreViewSet(viewsets.ModelViewSet):
    serializer_class= MembreSerializer
    filter_fields=["user"]

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [IsUtilisateurAuthenticated | IsModerateurAuthenticated | IsAdminAututhenticated | IsSuperAdminAututhenticated]
        elif self.request.method == "POST":
            self.permission_classes = [IsAdminAututhenticated | IsSuperAdminAututhenticated]
        elif self.request.method == "PUT" or self.request.method == "PATCH":
            self.permission_classes = [IsUtilisateurAuthenticated | IsModerateurAuthenticated | IsAdminAututhenticated | IsSuperAdminAututhenticated]
        elif self.request.method=="DELETE":
            self.permission_classes = [IsAdminAututhenticated | IsSuperAdminAututhenticated]
        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        queryset= Membre.objects.all()

        membre_id = self.request.GET.get('id_membre')
        if membre_id is not None:
            queryset = queryset.filter(id=membre_id)
        return queryset

    def destroy(self, request, *args, **kwargs):
        membre=self.get_object()
        User.objects.filter(username=membre.user.username).delete()
        membre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ModerateurViewSet(viewsets.ModelViewSet):
    serializer_class= ModerateurSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [IsModerateurAuthenticated | IsAdminAututhenticated | IsSuperAdminAututhenticated]
        elif self.request.method == "POST":
            self.permission_classes = [IsSuperAdminAututhenticated]
        elif self.request.method == "PUT" or self.request.method == "PATCH":
            self.permission_classes = [IsModerateurAuthenticated | IsAdminAututhenticated | IsSuperAdminAututhenticated]
        elif self.request.method=="DELETE":
            self.permission_classes = [IsSuperAdminAututhenticated]
        return [permission() for permission in self.permission_classes]
    
    def get_queryset(self):
        queryset= Moderateur.objects.all()
        moderateur_id = self.request.GET.get('id_moderateur')
        if moderateur_id is not None:
            queryset = queryset.filter(id=moderateur_id)
        return queryset
    
    def destroy(self, request, *args, **kwargs):
        moderateur=self.get_object()
        moderateur.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminViewSet(viewsets.ModelViewSet):
    serializer_class= AdminSerializer
    filter_fields=["utilisateur"]

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [IsAdminAututhenticated | IsSuperAdminAututhenticated]
        elif self.request.method == "POST":
            self.permission_classes = [IsSuperAdminAututhenticated]
        elif self.request.method == "PUT" or self.request.method == "PATCH":
            self.permission_classes = [IsAdminAututhenticated | IsSuperAdminAututhenticated]
        elif self.request.method=="DELETE":
            self.permission_classes = [IsSuperAdminAututhenticated]
        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        queryset= Admin.objects.all()
        admin_id = self.request.GET.get('id_admin')
        if admin_id is not None:
            queryset = queryset.filter(id=admin_id)
        return queryset

    def destroy(self, request, *args, **kwargs):
        admin=self.get_object()
        admin.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SuperAdminViewSet(viewsets.ModelViewSet):
    serializer_class= SuperAdminSerializer
    filter_fields=["admin"]

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [IsUtilisateurAuthenticated | IsModerateurAuthenticated | IsAdminAututhenticated | IsSuperAdminAututhenticated]
        elif self.request.method == "POST":
            self.permission_classes = [IsModerateurAuthenticated | IsAdminAututhenticated | IsSuperAdminAututhenticated]
        elif self.request.method == "PUT" or self.request.method == "PATCH":
            self.permission_classes = [IsUtilisateurAuthenticated | IsModerateurAuthenticated | IsAdminAututhenticated | IsSuperAdminAututhenticated]
        elif self.request.method=="DELETE":
            self.permission_classes = [IsAdminAututhenticated | IsSuperAdminAututhenticated]
        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        queryset= SuperAdmin.objects.all()
        super_admin_id = self.request.GET.get('id_super_admin')
        if super_admin_id is not None:
            queryset = queryset.filter(id=super_admin_id)
        return queryset

    def destroy(self, request, *args, **kwargs):
        super_admin=self.get_object()
        super_admin.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class CategorieViewSet(viewsets.ModelViewSet):
    serializer_class= CategorieSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes= [IsAdminAututhenticated | IsModerateurAuthenticated ]
        elif self.request.method == "PUT" or self.request.method == "PATCH":
            self.permission_classes=[IsAdminAututhenticated | IsModerateurAuthenticated ]
        elif self.request.method=="DELETE":
            self.permission_classes= [IsAdminAututhenticated | IsModerateurAuthenticated ]
        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        queryset= Categorie.objects.all()
        categorie_id = self.request.GET.get('categorie_id')
        if categorie_id is not None:
            queryset = queryset.filter(id=categorie_id)
        return queryset
    
    def destroy(self, request, *args, **kwargs):
        categorie=self.get_object()
        categorie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(viewsets.ModelViewSet):
    serializer_class= TagSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes= [IsAdminAututhenticated | IsModerateurAuthenticated ]
        elif self.request.method == "PUT" or self.request.method == "PATCH":
            self.permission_classes=[IsAdminAututhenticated | IsModerateurAuthenticated ]
        elif self.request.method=="DELETE":
            self.permission_classes= [IsAdminAututhenticated | IsModerateurAuthenticated ]
        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        queryset= Tag.objects.all()
        tag_id = self.request.GET.get('id_tag')
        if tag_id is not None:
            queryset = queryset.filter(id=tag_id)
        return queryset
    
    def destroy(self, request, *args, **kwargs):
        tag=self.get_object()
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DiscussionViewSet(viewsets.ModelViewSet):
    serializer_class= DiscussionSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [IsUtilisateurAuthenticated | IsModerateurAuthenticated | IsAdminAututhenticated | IsSuperAdminAututhenticated]
        elif self.request.method == "POST":
            self.permission_classes = [IsModerateurAuthenticated | IsAdminAututhenticated | IsSuperAdminAututhenticated]
        elif self.request.method == "PUT" or self.request.method == "PATCH":
            self.permission_classes = [IsModerateurAuthenticated | IsAdminAututhenticated | IsSuperAdminAututhenticated]
        elif self.request.method=="DELETE":
            self.permission_classes = [IsAdminAututhenticated | IsSuperAdminAututhenticated]
        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        queryset= Discussion.objects.all()
        discussion_id = self.request.GET.get('id_discussion')
        if discussion_id is not None:
            queryset = queryset.filter(id=discussion_id)
        return queryset
    
    def destroy(self, request, *args, **kwargs):
        discussion=self.get_object()
        discussion.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostViewSet(viewsets.ModelViewSet):
    serializer_class= PostSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [IsUtilisateurAuthenticated | IsModerateurAuthenticated | IsAdminAututhenticated | IsSuperAdminAututhenticated]
        elif self.request.method == "POST":
            self.permission_classes = [IsAdminAututhenticated | IsSuperAdminAututhenticated]
        elif self.request.method == "PUT" or self.request.method == "PATCH":
            self.permission_classes = [IsUtilisateurAuthenticated | IsModerateurAuthenticated | IsAdminAututhenticated | IsSuperAdminAututhenticated]
        elif self.request.method=="DELETE":
            self.permission_classes = [IsAdminAututhenticated | IsSuperAdminAututhenticated]
        return [permission() for permission in self.permission_classes]
        
    def get_queryset(self):
        queryset= Post.objects.all()
        post_id = self.request.GET.get('id_post')
        if post_id is not None:
            queryset = queryset.filter(id=post_id)
        return queryset
    
    def destroy(self, request, *args, **kwargs):
        post=self.get_object()
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class= QuestionSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [IsUtilisateurAuthenticated | IsModerateurAuthenticated | IsAdminAututhenticated | IsSuperAdminAututhenticated]
        elif self.request.method == "POST":
            self.permission_classes = [IsAdminAututhenticated | IsSuperAdminAututhenticated]
        elif self.request.method == "PUT" or self.request.method == "PATCH":
            self.permission_classes = [IsUtilisateurAuthenticated | IsModerateurAuthenticated | IsAdminAututhenticated | IsSuperAdminAututhenticated]
        elif self.request.method=="DELETE":
            self.permission_classes = [IsAdminAututhenticated | IsSuperAdminAututhenticated]
        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        queryset= Question.objects.all()
        question_id = self.request.GET.get('id_question')
        if question_id is not None:
            queryset = queryset.filter(id=question_id)
        return queryset
    
    def destroy(self, request, *args, **kwargs):
        question=self.get_object()
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReponseViewSet(viewsets.ModelViewSet):
    serializer_class= ReponseSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [IsUtilisateurAuthenticated | IsModerateurAuthenticated | IsAdminAututhenticated | IsSuperAdminAututhenticated]
        elif self.request.method == "POST":
            self.permission_classes = [IsAdminAututhenticated | IsSuperAdminAututhenticated]
        elif self.request.method == "PUT" or self.request.method == "PATCH":
            self.permission_classes = [IsUtilisateurAuthenticated | IsModerateurAuthenticated | IsAdminAututhenticated | IsSuperAdminAututhenticated]
        elif self.request.method=="DELETE":
            self.permission_classes = [IsAdminAututhenticated | IsSuperAdminAututhenticated]
        return [permission() for permission in self.permission_classes]
    def get_queryset(self):
        queryset= Reponse.objects.all()
        reponse_id = self.request.GET.get('id_reponse')
        if reponse_id is not None:
            queryset = queryset.filter(id=reponse_id)
        return queryset
    
    def destroy(self, request, *args, **kwargs):
        reponse=self.get_object()
        reponse.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LikesViewSet(viewsets.ModelViewSet):
    queryset = Likes.objects.all()
    serializer_class = LikesSerializer
    permission_classes = [permissions.IsAuthenticated]

class DislikesViewSet(viewsets.ModelViewSet):
    queryset = Dislikes.objects.all()
    serializer_class = DislikesSerializer
    permission_classes = [permissions.IsAuthenticated]

class SignaleViewSet(viewsets.ModelViewSet):
    queryset = Signale.objects.all()
    serializer_class = SignaleSerializer
    permission_classes = [permissions.IsAuthenticated]

class NotificationsViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

class MessageViewSet(viewsets.ModelViewSet):
    queryset =Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

class LoginAPIView(viewsets.ModelViewSet):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)