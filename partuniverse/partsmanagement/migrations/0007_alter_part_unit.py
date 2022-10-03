# Generated by Django 4.1.1 on 2022-10-03 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("partsmanagement", "0006_auto_20180909_1200"),
    ]

    operations = [
        migrations.AlterField(
            model_name="part",
            name="unit",
            field=models.CharField(
                choices=[
                    ("Piece", (("pc", "piece"),)),
                    ("Length", (("m", "meters"), ("cm", "centimeters"))),
                    (
                        "Volume",
                        (
                            ("l", "litres"),
                            ("m³", "cubicmeters"),
                            ("ccm", "cubic centimeters"),
                        ),
                    ),
                    ("n/A", "Unknown"),
                ],
                default="---",
                help_text="The unit quantities are in.",
                max_length=3,
                verbose_name="Messuring unit",
            ),
        ),
    ]
