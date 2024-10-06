# Generated by Django 5.1.1 on 2024-10-03 09:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0003_listing_created_at_listing_current_price"),
    ]

    operations = [
        migrations.RenameField(
            model_name="bid",
            old_name="bid",
            new_name="bid_amount",
        ),
        migrations.RenameField(
            model_name="bid",
            old_name="time_stamp",
            new_name="timestamp",
        ),
        migrations.RenameField(
            model_name="comment",
            old_name="content",
            new_name="comment_text",
        ),
        migrations.RenameField(
            model_name="comment",
            old_name="user",
            new_name="commentor",
        ),
        migrations.AlterField(
            model_name="bid",
            name="listing",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="bids",
                to="auctions.listing",
            ),
        ),
        migrations.AlterField(
            model_name="bid",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="bids",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.CreateModel(
            name="Watchlist",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "listing",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="watchlisted_by",
                        to="auctions.listing",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="watchlist",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
