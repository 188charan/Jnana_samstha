from django.db import models 


class StudyMaterial(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, null=True)
    link = models.URLField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title 
    
    

