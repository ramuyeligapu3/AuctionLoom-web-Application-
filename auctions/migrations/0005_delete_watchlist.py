# Generated by Django 5.1.1 on 2024-10-04 05:13

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0004_rename_bid_bid_bid_amount_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Watchlist",
        ),
    ]
