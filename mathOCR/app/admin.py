from django.contrib import admin
from .models import Images, RecognitionResults, User

# Register your models here.

admin.site.register(Images)
admin.site.register(RecognitionResults)
admin.site.register(User)
