from django.contrib import admin
from book_app.models import Book,Review
# Register your models here.
class Bookmodeladmin(admin.ModelAdmin):
    list_display=['title','author']

class Reviewmodeladmin(admin.ModelAdmin):
    list_display=['book','rating','comment']


admin.site.register(Book,Bookmodeladmin)
admin.site.register(Review,Reviewmodeladmin)