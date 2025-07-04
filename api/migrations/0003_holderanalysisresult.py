# Generated by Django 5.2.3 on 2025-06-28 22:14

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_contractanalysisresult_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HolderAnalysisResult',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('top_holders', models.JSONField()),
                ('centralization_score', models.FloatField()),
                ('anomalies', models.JSONField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('token', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='holder_analyses', to='api.tokencomplianceprofile')),
            ],
        ),
    ]
