from django.shortcuts import render
from django.db.models import Count, Avg
from .models import Category, Product


# Create your views here.
def index(request):
    # products = Product.objects.all().order_by("price") # Ascending order
    # products = Product.objects.all().order_by("-price") # Descending order

    # categories = Category.objects.all().annotate(product_count=Count("product"))
    categories = (
        Category.objects.all()
        .annotate(product_count=Count("product"))
        .prefetch_related("product_set")
    )

    products = (
        Product.objects.all().order_by("price", "title").select_related("category")
    )
    # products = Product.objects.filter(category__title="Electronics")

    price_avg = products.aggregate(Avg("price"))["price__avg"]
    # price_avg = Product.objects.raw("SELECT AVG(price) FROM products_product")

    context = {
        "categories": categories,
        "products": products,
        "price_avg": round(price_avg, 2),
    }
    return render(request, "products/index.html", context=context)
