from django.db import models
from django.db.models import Prefetch
from base_module.models.deletion import SoftDeletionModel,SoftDeletionManager
from base_module.models.mixin import RescaleImageMixin

class AboutUsManager(SoftDeletionManager):
    def get_queryset(self, *args , **kwargs):
        return super().get_queryset(*args , **kwargs).prefetch_related(
            Prefetch('skills_set' ,queryset=Skills.objects.filter(is_active=True)
                                                                            )
                                                                       )

class AboutUs(RescaleImageMixin , SoftDeletionModel):

    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/about_us/')
    github_link = models.URLField(max_length=500)
    description = models.TextField()
    is_active = models.BooleanField(default=True , db_index=True)

    objects = AboutUsManager()

    def __init__(self , *args , **kwargs):
        super().__init__(*args , **kwargs)
        self.image_field_name = 'image'
        self.max_width = 240
        self.max_size = 100000 # around 100 KB

    def save(self ,*args , **kwargs):
        # only one instance of SiteSetting can be / ACTIVE /
        if self.is_active:
            AboutUs.objects.exclude(id = self.id).update(is_active = False)

        self.title = self.title.title()
        super().save(*args , **kwargs)

    def __str__(self):
        return self.title + ' : ' +self.description[:20]


class Skills(RescaleImageMixin , SoftDeletionModel):
    about_us = models.ForeignKey(to=AboutUs , on_delete=models.PROTECT)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/about_us/skills/', blank=True , null=True)
    fa_icon = models.CharField(max_length=50,blank=True ,null=True)
    link = models.URLField(max_length=500,null=True , blank=True)
    is_active = models.BooleanField(default=True)

    def __init__(self , *args , **kwargs):
        super().__init__(*args , **kwargs)
        self.image_field_name = 'image'
        self.max_width = 160
        self.max_size = 50000 # around 50 KB

    def __str__(self):
        return self.title
