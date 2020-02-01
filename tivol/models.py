from django.db import models


class ContentMigrationStatus(models.Model):
    """
    Keep tracking of rows from sources and to where they were migrated. This
    will help us rollback any migrated content or to know if a content has been
    migrated or not.
    """
    source_id = models.CharField(max_length=255)
    destination_id = models.IntegerField()
    model_target = models.CharField(max_length=255)
    handler = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.model_target.split('.')[1]} - {self.source_id}"
