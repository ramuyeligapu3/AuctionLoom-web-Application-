# admin.py
from django.contrib import admin
from .models import Listing, Comment, Bid,Watchlist

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'creator', 'starting_bid','current_price', 'is_active', 'created_at')
    list_filter = ('category', 'is_active')
    search_fields = ('title', 'description', 'category')

admin.site.register(Comment)
admin.site.register(Bid)

admin.site.register(Watchlist)
