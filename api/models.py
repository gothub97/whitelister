import uuid
from django.db import models
from uuid import uuid4
import hashlib

class TokenComplianceProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    token_address = models.CharField(max_length=42, unique=True)
    name = models.CharField(max_length=128, null=True, blank=True)
    symbol = models.CharField(max_length=32, null=True, blank=True)
    decimals = models.IntegerField(null=True, blank=True)
    risk_score = models.FloatField(default=0.0)
    recommendation = models.CharField(
        max_length=32,
        choices=[
            ("go", "GO"),
            ("no_go", "NO GO"),
            ("enhanced_due_diligence", "Enhanced Due Diligence"),
            ("pending", "Pending"),
        ],
        default="pending"
    )
    flags = models.JSONField(default=list, blank=True)
    modules = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.symbol or 'Token'} @ {self.token_address[:8]}..."

class ContractAnalysisResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    token = models.ForeignKey(
        'TokenComplianceProfile',
        on_delete=models.CASCADE,
        related_name='contract_analyses'  # <-- 1:N
    )
    score = models.FloatField()
    flags = models.JSONField(default=list)
    evidence = models.JSONField(default=list)
    bytecode = models.TextField(blank=True, null=True)
    bytecode_hash = models.CharField(max_length=64, blank=True, null=True)
    engine_version = models.CharField(max_length=16, default="0.1-beta")
    analyzed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-analyzed_at"]

class HolderAnalysisResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    token = models.ForeignKey("TokenComplianceProfile", on_delete=models.CASCADE, related_name="holder_analyses")
    top_holders = models.JSONField()
    centralization_score = models.FloatField()
    anomalies = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)


class Holder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class HolderAddress(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    holder = models.ForeignKey(Holder, on_delete=models.CASCADE, related_name="addresses")
    address = models.CharField(max_length=42, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class HolderTokenLink(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    holder_address = models.ForeignKey(HolderAddress, on_delete=models.CASCADE, related_name="tokens")
    token = models.ForeignKey("TokenComplianceProfile", on_delete=models.CASCADE, related_name="holder_links")
    balance = models.DecimalField(max_digits=80, decimal_places=0)
    created_at = models.DateTimeField(auto_now_add=True)