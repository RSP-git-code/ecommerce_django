from django.shortcuts import render
from items.models import Item, Category
from .models import Profile
from .forms import SignupForm, UserUpdateForm, ProfileUpdateForm
from django.db.models import Q 
def index(request):
    items = Item.objects.filter(sold=False)[:6]
    categories = Category.objects.all()
    return render(request, 'index.html', {
        'items': items,
        'categories': categories
    })
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
import re

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('core:login')  # Redirect to success page or login
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
def login_view(request):
    return render(request, 'login.html')

from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from .models import Profile 

def profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('core:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)

    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

from rapidfuzz import fuzz

def browse_items(request):
    query = request.GET.get('q', '').strip()
    items = Item.objects.all()
    matched_items = []

    if query:
        for item in items:
            score_name = fuzz.partial_ratio(query.lower(), item.name.lower())
            score_category = fuzz.partial_ratio(query.lower(), item.category.name.lower())
            if score_name >= 70 or score_category >= 70:  # threshold (tweak if needed)
                matched_items.append(item)
    else:
        matched_items = items

    return render(request, 'browse_items.html', {'items': matched_items, 'query': query})
from django.shortcuts import get_object_or_404

def add_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    cart = request.session.get('cart', [])
    if item.id not in cart:
        cart.append(item.id)
    request.session['cart'] = cart
    return redirect('core:view_cart')
def view_cart(request):
    cart = request.session.get('cart', [])
    cart_items = []
    total = 0

    for item_id in cart:
        item = get_object_or_404(Item, pk=item_id)
        total += item.price
        cart_items.append({
            'item': item,
            'quantity': 1,  # You can later add quantity logic if needed
            'item_total': item.price,
        })

    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})
def remove_from_cart(request, item_id):
    cart = request.session.get('cart', [])
    if item_id in cart:
        cart.remove(item_id)
    request.session['cart'] = cart
    return redirect('core:view_cart')

