from django import forms

class CreateListingForm(forms.Form):
    title = forms.CharField(max_length=100, label='Title',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}))
    description = forms.CharField( widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter description', 'rows': 4}), label='Description')
    starting_bid = forms.DecimalField(max_digits=10, decimal_places=2, label='Starting Bid',widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter starting bid'}))
    image_url = forms.URLField(required=False, label='Image URL',widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Optional: Enter image URL'}))
    category = forms.CharField(max_length=50, label='Category',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter category'}))


class BidForm(forms.Form):
    bid_amount = forms.DecimalField(max_digits=10, decimal_places=2, label='Bid Amount')


class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label='Comment')
