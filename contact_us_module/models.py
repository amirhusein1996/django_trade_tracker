from django.db import models
from account_module.models import User
from base_module.models.mixin import RescaleImageMixin


class ContactUsMessage (RescaleImageMixin , models.Model):
    user = models.ForeignKey(to=User , on_delete=models.PROTECT)
    subject = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/contact_us/' , blank=True , null=True)
    message = models.TextField()
    response = models.TextField(blank=True , null=True)
    is_read_by_admin = models.BooleanField(blank=True , null=True)
    has_responded = models.BooleanField(blank=True , null=True , editable=False)

    def save(self, *args , **kwargs):
        if self.response:
            self.has_responded = True

        super().save(*args , **kwargs)

    def __str__(self):
        return self.subject
