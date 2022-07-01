from django.contrib import admin
from .models import *

admin.site.register(Anonyme)
admin.site.register(Admin)
admin.site.register(SuperAdmin)
admin.site.register(Categorie)
admin.site.register(Discussion)

admin.site.register(Signale)
admin.site.register(Reponse)
admin.site.register(Question)
admin.site.register(Rate)
admin.site.register(Profile)
admin.site.register(Notification)
admin.site.register(Likes)
admin.site.register(Tag)

@admin.register(Membre)
class Membres(admin.ModelAdmin):
    list_display = ("user","nom","prenom","telephone")
@admin.register(Post)
class Posts(admin.ModelAdmin):
    list_display = ("id","likes_count")