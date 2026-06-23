from django.contrib import admin
from .models import Post

# Register your models here.

#admin.site.register(Post)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status', 'views', 'image_preview']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', '-publish']
    show_facets = admin.ShowFacets.ALWAYS
    
    readonly_fields = ['image_preview']
    
    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }
    
    def image_preview(self, obj):
        from django.utils.html import format_html
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;"/>', obj.image.url)
        return '(Without image)'
    
    image_preview.short_description = 'Preview'