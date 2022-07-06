from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from .models import *
from .serializers import *
from rest_framework.viewsets import ModelViewSet
from .permissions import *
from rest_framework.response import Response
from rest_framework import status
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    permission_classes = [permissions.IsAuthenticated]
class MembreViewSet(viewsets.ModelViewSet):
    serializer_class= MembreSerializer
    filter_fields=["user","telephone"]

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [ IsAdminAututhenticated ]
        elif self.request.method=="DELETE":
            self.permission_classes= [ IsAdminAututhenticated ]
        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
            queryset= Membre.objects.all()
            telephone = self.request.GET.get('telephone')
            if telephone is not None:
                queryset = queryset.filter(membre__telephone=telephone)
            return queryset
class ModerateurViewSet(viewsets.ModelViewSet):
    queryset = Moderateur.objects.all()
    serializer_class = ModerateurSerializer
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
        programme=self.get_object()
        programme.delete()
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
        projet=self.get_object()
        projet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DiscussionViewSet(viewsets.ModelViewSet):
    queryset = Discussion.objects.all()
    serializer_class = DiscussionSerializer
    permission_classes = [permissions.IsAuthenticated]

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

class ReponseViewSet(viewsets.ModelViewSet):
    queryset = Reponse.objects.all()
    serializer_class = ReponseSerializer
    permission_classes = [permissions.IsAuthenticated]

class LikesViewSet(viewsets.ModelViewSet):
    queryset = Likes.objects.all()
    serializer_class = LikesSerializer
    permission_classes = [permissions.IsAuthenticated]

class NotificationsViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

class MessageViewSet(viewsets.ModelViewSet):
    queryset =Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    

