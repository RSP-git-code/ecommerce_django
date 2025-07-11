from django.shortcuts import render, get_object_or_404
from .models import Item, Category

def index(request):
    items = Item.objects.filter(sold=False)[0:6]
    categories = Category.objects.all()
    return render(request, 'index.html', {
        'categories': categories,
        'items': items,
    })
def detail(request, id):
    item = get_object_or_404(Item, id=id)
    categories = Category.objects.all()
    related_items = Item.objects.filter(
        category=item.category,
        sold=False
    ).exclude(id=id)[:3]

    return render(request, 'detail.html', {
        'item': item,
        'categories': categories,
        'related_items': related_items,
    })



