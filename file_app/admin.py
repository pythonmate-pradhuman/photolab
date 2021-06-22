from django.contrib import admin

# Register your models here.
from .models import File, Hashtag, FileHashtags
from django.utils.safestring import mark_safe
from django.utils.html import format_html


# admin.site.register(File)
# admin.site.register(Hashtag)
# admin.site.register(FileHashtags)

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('action', 'custom_filter','Input_Image','Output_Image',)

    list_filter = ('action',)

    search_fields = ('action',)
    ordering = ('action',)

    readonly_fields = ['Input_Image','Output_Image',]

    def Input_Image(self, obj):
        print(obj.file)
        return mark_safe('<img src="http://127.0.0.1:8000/media/{url}" width="100px" height="auto" />'.format(
            url=obj.file
        ))


    def Output_Image(self, obj):
        print(obj.processed_image)
        return mark_safe('<img src="{url}" width="100px" height="auto" />'.format(
            url=obj.processed_image
        ))