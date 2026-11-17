
from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0002_remove_trip_status'),
        ('destinations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID',
                )),
                ('score', models.DecimalField(
                    max_digits=5,
                    decimal_places=2,
                )),
                ('reason', models.TextField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('attraction', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='recommendations',
                    to='destinations.attraction',
                )),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='recommendations',
                    to=settings.AUTH_USER_MODEL,
                )),
                ('trip', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='recommendations',
                    to='trips.trip',
                )),
            ],
            options={
                'ordering': ('-score',),
            },
        ),
    ]
