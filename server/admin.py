from django.contrib import admin
from .models import *

admin.site.register(Anonyme)
admin.site.register(Moderateur)
admin.site.register(Admin)
admin.site.register(SuperAdmin)
admin.site.register(Categorie)
admin.site.register(Discussion)
admin.site.register(Signale)
admin.site.register(Question)
admin.site.register(Profile)
admin.site.register(Likes)
admin.site.register(Tag)
admin.site.register(Dislikes)

@admin.register(Membre)
class Membres(admin.ModelAdmin):
    list_display = ("user","telephone")

@admin.register(Post)
class Posts(admin.ModelAdmin):
    list_display = ("body","user","likes_count","dislikes_count","signale_count")

@admin.register(Reponse)
class Reponses(admin.ModelAdmin):
    list_display = ("body","user","post","likes_count")

@admin.register(Message)
class Messages(admin.ModelAdmin):
    list_display = ("sender","recipient","body")

@admin.register(Notification)
class Notifications(admin.ModelAdmin):
    list_display = ("sender","recevier","post","notification_type")
