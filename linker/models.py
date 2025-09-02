from django.db import models


class Tag(models.Model):
    """태그를 저장하는 테이블 model"""

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Link(models.Model):
    """링크를 저장하는 테이블 model"""

    id = models.AutoField(primary_key=True)
    url = models.URLField(max_length=1000, null=False)
    title = models.CharField(max_length=100, null=True)
    summary = models.TextField(blank=True, null=True)
    image_url = models.URLField(max_length=1000, blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="links")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
