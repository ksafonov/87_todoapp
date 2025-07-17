from django.db import models

class TodoItem(models.Model):

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    marked_as_done_at = models.DateTimeField(null=True, blank=True)

    is_done = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

