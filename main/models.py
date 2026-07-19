from django.db import models
from django.contrib.auth.models import User
import uuid

class ScanHistory(models.Model):
    SEVERITY_CHOICES = [
        ('Low', 'Low'),
        ('Moderate', 'Moderate'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='uploads/', null=True, blank=True)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    detected_issue = models.TextField()
    confidence = models.FloatField()
    first_aid = models.JSONField()
    red_flags = models.JSONField()
    recommended_action = models.TextField()
    symptoms = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

class Alert(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    channel = models.CharField(max_length=50, default='whatsapp')
    recipient = models.CharField(max_length=100)
    severity = models.CharField(max_length=20)
    message = models.TextField()
    status = models.CharField(max_length=50)

    class Meta:
        ordering = ['-created_at']
