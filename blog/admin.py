from django.contrib import admin

from blog.models import Post, Category, Tag, Comments
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms


class PostAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    form = PostAdminForm
    list_display = ['id', 'title', 'category', 'created_date', 'likes', 'views']
    list_display_links = ['id', 'title']


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('tag_name',)}


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
# admin.site.register(UserPostRelation)
admin.site.register(Comments)
