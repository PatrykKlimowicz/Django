from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.


class Action(models.Model):
    # user who performed action
    user = models.ForeignKey('auth.User', related_name='actions', db_index=True, on_delete=models.CASCADE)

    # describe the action
    verb = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    # points to the ContentType model
    target_ct = models.ForeignKey(ContentType,
                                  blank=True,
                                  null=True,
                                  related_name='target_obj',
                                  on_delete=models.CASCADE)

    # Primary Key for the related object
    target_id = models.PositiveIntegerField(null=True,
                                            blank=True,
                                            db_index=True)

    # field to related object based on combination of target_ct and target_id
    target = GenericForeignKey('target_ct', 'target_id')

    class Meta:
        ordering = ('-created',)
