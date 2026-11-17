
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("trips", "0001_initial"),
    ]

    operations = [
        # No operation needed.
        # The new 0001_initial already creates Trip without status.
        # The old database records this migration as applied.
    ]
