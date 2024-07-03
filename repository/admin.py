from django.contrib import admin
from .models import StudyMaterial

@admin.register(StudyMaterial)
class StudyMaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'tags', 'link')
    search_fields = ('title', 'tags')

# Alternatively, we can use the simpler syntax if we don't need custom admin behavior:
#admin.site.register(StudyMaterial)
