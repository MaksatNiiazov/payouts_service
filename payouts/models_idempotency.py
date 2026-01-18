from django.db import models


class IdempotencyKey(models.Model):
    key = models.CharField(max_length=255, unique=True)
    response_status = models.PositiveSmallIntegerField()
    response_body = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "idempotency_keys"
        indexes = [
            models.Index(fields=["key"]),
        ]

    def __str__(self) -> str:
        return self.key
