from django.contrib import admin
from .models import CustomFilters
from django.utils.safestring import mark_safe
# Register your models here.

admin.site.site_header = "Photolab alter"
admin.site.site_title = "Photolab alter portal"
admin.site.index_title = "Welcome to Photolab alter Portal"
# admin.site.disable_action('delete_selected')


@admin.register(CustomFilters)
class CustomFiltersAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'action',
                    'Input_Image', 'Output_Image')

    list_filter = ('is_active', 'action')

    search_fields = ('name', 'action', 'created_by')
    ordering = ('name',)

    readonly_fields = ['Input_Image', 'background_image_1',
                       'background_image_2', 'background_image_3', 'background_image_4', 'background_image_5', 'background_image_6','background_image_7','background_image_8','Output_Image']

    def Input_Image(self, obj):
        try:
            return mark_safe('<img src="{url}" width="100px" height="auto" />'.format(
                url=obj.input_file.url,
                width=obj.input_file.width,
                height=obj.input_file.height,
            )

            )
        except:
            return ""

    def Output_Image(self, obj):
        try:
            return mark_safe('<img src="{url}" width="100px" height="auto" />'.format(
            url=obj.processed_image.url,
            width=obj.processed_image.width,
            height=obj.processed_image.height,
            )
            )
        except:
            return ""

    def background_image_1(self, obj):
        return mark_safe('<img src="{url}" width="100px" height="auto" />'.format(
            url=obj.bg_image_1.url,
            width=obj.bg_image_1.width,
            height=obj.bg_image_1.height,
        )
        )

    def background_image_2(self, obj):
        return mark_safe('<img src="{url}" width="100px" height="auto" />'.format(
            url=obj.bg_image_2.url,
            width=obj.bg_image_2.width,
            height=obj.bg_image_2.height,
        )
        )

    def background_image_3(self, obj):
        return mark_safe('<img src="{url}" width="100px" height="auto" />'.format(
            url=obj.bg_image_3.url,
            width=obj.bg_image_3.width,
            height=obj.bg_image_3.height,
        )
        )

    def background_image_4(self, obj):
        return mark_safe('<img src="{url}" width="100px" height="auto" />'.format(
            url=obj.bg_image_4.url,
            width=obj.bg_image_4.width,
            height=obj.bg_image_4.height,
        )
        )

    def background_image_5(self, obj):
        return mark_safe('<img src="{url}" width="100px" height="auto" />'.format(
            url=obj.bg_image_5.url,
            width=obj.bg_image_5.width,
            height=obj.bg_image_5.height,
        )
        )

    def background_image_6(self, obj):
        return mark_safe('<img src="{url}" width="100px" height="auto" />'.format(
            url=obj.bg_image_6.url,
            width=obj.bg_image_6.width,
            height=obj.bg_image_6.height,
        )
        )

    def background_image_7(self, obj):
        return mark_safe('<img src="{url}" width="100px" height="auto" />'.format(
            url=obj.bg_image_7.url,
            width=obj.bg_image_7.width,
            height=obj.bg_image_7.height,
        )
        )

    def background_image_8(self, obj):
        return mark_safe('<img src="{url}" width="100px" height="auto" />'.format(
            url=obj.bg_image_8.url,
            width=obj.bg_image_8.width,
            height=obj.bg_image_8.height,
        )
        )