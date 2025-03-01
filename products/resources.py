"""This module defines the functions for fetching products from the database"""
from .models import Products, ProductCategory
from django.db.models import Count
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Value

def fetch_vendor_products(vendor):
    """This function fetches all products for a vendor"""
    
    products = Products.objects.filter(store=vendor)
    return products

def fetch_vendor_product(vendor, product_id):
    """This function fetches a single product for a vendor"""
    product = Products.objects.get(store=vendor, id=product_id)
    return product

def fetch_all_products():
    """This function fetches all products"""
    products = Products.objects.all()
    return products

def fetch_product_categories():
    """This function fetches all product categories"""
    categories = ProductCategory.objects.all()
    return categories

def fetch_product_category(category_id):
    """This function fetches a single product category"""
    category = ProductCategory.objects.get(id=category_id)
    return category

def fetch_child_categories(parent_category_id):
    """This function fetches all child categories of a parent category"""
    categories = ProductCategory.objects.filter(parent_id=parent_category_id)
    return categories

def fetch_product_categories_with_products(min_products=4):
    """This function fetches all product categories that have at least min_products"""
    categories = ProductCategory.objects.annotate(num_products=Count('products')).filter(num_products__gte=min_products)
    return categories

def fetch_random_category(request):
    """Fetches a random category that has at least 4 products."""
    categories = fetch_product_categories_with_products()

    print(f'Categories count: {categories.count()}')

    if not categories.exists():
        return None  # Handle case where there are no categories

    # Ensure session key exists
    if 'random_categories' not in request.session:
        request.session['random_categories'] = []

    # Avoid infinite recursion when all categories are used
    if len(request.session['random_categories']) == categories.count():
        request.session['random_categories'] = []  # Reset session if all are used

    # Get a random category that is not in session
    available_categories = categories.exclude(id__in=request.session['random_categories'])
    if not available_categories.exists():
        return None  # Safety check in case all are exhausted

    category = available_categories.order_by('?').first()

    # Add category to session and ensure session updates
    request.session['random_categories'].append(category.id)
    request.session.modified = True  # Required to ensure Django saves session changes

    return category

def fetch_products_by_category(category_id):
    """This function fetches all products in a category including child category products if any"""
    category_products = []
    child_categories = fetch_child_categories(category_id)
    if child_categories:
        for category in child_categories:
            category_products.extend(fetch_products_by_category(category.id))
    else:
        #category_products = Products.objects.filter(category_id=category_id)
        category_products = fetch_all_products().filter(category_id=category_id)
    return category_products

def fetch_hot_deals_products():
    """This function fetches all products that are hot deals"""
    hot_deals = fetch_all_products().order_by('?')
    return hot_deals

def fetch_most_popular_products():
    """This function fetches all products that are most popular"""
    most_popular = fetch_all_products().order_by('?')
    return most_popular

# function to create category hierarchy
def get_category_hierarchy(parent=None, level=0):
    """This function creates a hierarchy of product categories"""
    categories = fetch_product_categories().filter(parent=parent).order_by("name")
    hierarchy = []
    
    for category in categories:
        prefix = "—" * level  # Indent child categories
        hierarchy.append((category.id, f"{prefix} {category.name}"))
        hierarchy.extend(get_category_hierarchy(category, level + 1))  # Recurse for children

    return hierarchy

def search_products(query):
    """This function searches for products based on a query"""
    products = fetch_all_products()
    return products.annotate(
        similarity=TrigramSimilarity("name", Value(query)) + TrigramSimilarity("description", Value(query))
    ).filter(similarity__gt=0.2).order_by("-similarity")




