from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from . import forms
from . import models
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

@login_required
def categories(request):
    # Get all distinct categories from the listings
    categories = models.Listing.objects.values_list('category', flat=True).distinct()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

@login_required
def category_listings(request, category):
    # Filter listings by the selected category
    listings = models.Listing.objects.filter(category=category, is_active=True)
    return render(request, "auctions/category_listings.html", {
        "category": category,
        "listings": listings
    })

@login_required
def watchlist(request):
    user_watchlist = models.Watchlist.objects.filter(user=request.user)
    
    # Handle remove from watchlist
    if request.method == "POST" and 'remove' in request.POST:
        listing_id = request.POST.get('listing_id')
        models.Watchlist.objects.filter(user=request.user, listing_id=listing_id).delete()
        messages.success(request, "Removed from your watchlist.")
        return redirect('watchlist')

    return render(request, "auctions/watchlist.html", {
        "watchlist_items": user_watchlist
    })


# Listing details page
@login_required
def listing(request, listing_id):
    listing = models.Listing.objects.get(pk=listing_id)
    comments = models.Comment.objects.filter(listing=listing)
    user_watchlist = models.Watchlist.objects.filter(user=request.user, listing=listing).exists()
    print(user_watchlist)
    highest_bid = models.Bid.objects.filter(listing=listing).order_by('-bid_amount').first()

    if highest_bid:
        current_price = highest_bid.bid_amount
    else:
        current_price = listing.starting_bid

    is_creator = request.user == listing.creator

    # Handle auction closing
    if request.method == "POST" and 'close_auction' in request.POST and is_creator:
        listing.is_active = False
        listing.save()
        messages.success(request, "The auction has been closed.")
        return redirect('listing', listing_id=listing.id)

    # Handle bidding
    if request.method == "POST" and 'bid_amount' in request.POST:
        bid_amount = float(request.POST.get('bid_amount'))
        if bid_amount < current_price:
            messages.error(request, "Bid must be higher than the current price.")
        else:
            bid = models.Bid.objects.create(listing=listing, user=request.user, bid_amount=bid_amount)
            listing.current_price = bid_amount
            listing.save()
            messages.success(request, "Your bid has been placed.")
            return redirect('listing', listing_id=listing.id)

    if request.method == "POST" and 'wt' in request.POST and not(user_watchlist):
            models.Watchlist.objects.create(user=request.user, listing=listing)
            messages.success(request, "Added to your watchlist.")
            user_watchlist = models.Watchlist.objects.filter(user=request.user, listing=listing).exists()
        

    # Handle comments
    if request.method == "POST" and 'comment' in request.POST:
        comment_text = request.POST.get('comment_text')
        models.Comment.objects.create(listing=listing, commentor=request.user, comment_text=comment_text)
        messages.success(request, "Your comment has been posted.")
        return redirect('listing', listing_id=listing.id)

    user_is_winner = not listing.is_active and highest_bid and highest_bid.user == request.user

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "current_price": current_price,
        "comments": comments,
        "user_watchlist": user_watchlist,
        "is_creator": is_creator,
        "user_is_winner": user_is_winner
    })


def index(request):
    listings = models.Listing.objects.filter(is_active=True).order_by("-created_at")
    print(f"Active Listings Count: {listings.count()}")  # Debugging output
    return render(request, "auctions/index.html", {"listings": listings})

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = models.User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
 

def create_listing(request):
    if request.method=="POST":
        form=forms.CreateListingForm(request.POST)
        if form.is_valid():
            listing=models.Listing(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                starting_bid=form.cleaned_data['starting_bid'],
                image_url=form.cleaned_data.get('image_url', ''),
                category=form.cleaned_data['category'],
                creator=request.user
            )
            listing.save()
            return redirect('index')
    else:
        form = forms.CreateListingForm()
    
    return render(request, 'auctions/create_listing.html', {'form': form})

