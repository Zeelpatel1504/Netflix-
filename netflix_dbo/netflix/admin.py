
from django.contrib import admin
from .models import Users,Profile,Language,Genre,ProfileGenre
from .models import MediaGenre,MediaType,Media,Season,Episode,ProfileWatchlist
admin.site.register(Users)
admin.site.register(Genre)
admin.site.register(MediaType)
admin.site.register(Language)
admin.site.register(Profile)
admin.site.register(Media)
admin.site.register(Season)
admin.site.register(Episode)
admin.site.register(MediaGenre)
admin.site.register(ProfileWatchlist)
admin.site.register(ProfileGenre)
