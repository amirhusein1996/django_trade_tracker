from django.db import models
from django.utils import timezone
from django.db.models import Manager , QuerySet

# class SoftDeletionManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().using(self._db).exclude(is_deleted=True)
#
#     def delete(self):
#         self.get_queryset().update(is_deleted=True, deleted_at=timezone.now())


class SoftDeletionQuerySet(QuerySet):
    def delete(self):
        return self.update(is_deleted=True, deleted_at=timezone.now())

class SoftDeletionManager(Manager):
    def get_queryset(self):
        return SoftDeletionQuerySet(self.model , self._db).exclude(is_deleted=True)

class SoftDeletionModel(models.Model):
    is_deleted = models.BooleanField(null=True, blank=True, editable=False)
    deleted_at = models.DateTimeField(null=True, blank=True,editable=False)

    objects = SoftDeletionManager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=['is_deleted', 'deleted_at'])



