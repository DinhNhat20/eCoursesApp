from django.contrib import admin
from django.utils.html import mark_safe

from courses.models import Course, Category, Tag, Lesson, Comment, User

from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class CourseForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Course
        fields = '__all__'


class MyCourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_date', 'updated_date', 'active']
    search_fields = ['id', 'name']
    list_filter = ['created_date', 'name']
    readonly_fields = ['my_image']
    form = CourseForm

    def my_image(self, course):
        if course.image:
            return mark_safe(f"<img src='/static/{course.image.name}' width='200' />")


class MyLessonAdmin(admin.ModelAdmin):
    list_display = ['subject', 'content', 'course', 'image']
    search_fields = ['subject', 'course']
    list_filter = ['subject', 'course']


admin.site.register(Category)
admin.site.register(Course, MyCourseAdmin)
admin.site.register(Lesson, MyLessonAdmin)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(User)