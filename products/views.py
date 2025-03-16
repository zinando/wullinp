from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from _core.utils.helpers import get_user_object, get_product_object, sanitize_string
from _core.image_manager import ImageManager
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Products, ProductCategory
from .serializer import ProductCategorySerializer, ProductSerializer
from django.contrib import messages
import cloudinary.uploader
from . import resources as resource
from _core.resources import fetch_user

# Create your views here.

# route for fetching products for display on home page
@api_view(['GET'])
def ProductView(request):
    """This route fetches products for display on home page"""
    if request.method == 'GET' and request.GET.get('query') == 'fetch_public_products':

        # get all products
        products = resource.fetch_all_products() #Products.objects.all()
        serializer = ProductSerializer(products, many=True)

        # fetch categories to display on the slider
        slider_categories = resource.fetch_child_categories(1) # 1 is occasion based categories
        slider_categories = ProductCategorySerializer(slider_categories, many=True).data

        # fetch two random categories to display on the home page
        random_category_1 = resource.fetch_random_category(request)
        random_category_2 = resource.fetch_random_category(request)

        # fetch products for the two random categories
        random_category_1_products = resource.fetch_products_by_category(random_category_1.id)
        random_category_2_products = resource.fetch_products_by_category(random_category_2.id)

        # fetch hot-deals and most popular products
        hot_deals = resource.fetch_hot_deals_products()[4:]
        most_popular = resource.fetch_most_popular_products()[4:]

        # fetch category hierarchy
        category_hierarchy = resource.get_category_hierarchy()

        # serialize the objects
        random_category_1 = ProductCategorySerializer(random_category_1).data
        random_category_2 = ProductCategorySerializer(random_category_2).data
        random_category_1_products = ProductSerializer(random_category_1_products, many=True).data
        random_category_2_products = ProductSerializer(random_category_2_products, many=True).data
        hot_deals = ProductSerializer(hot_deals, many=True).data
        most_popular = ProductSerializer(most_popular, many=True).data

        response_data = {
            'slider_categories': slider_categories,
            'products':serializer.data,
            'random_category_1': random_category_1,
            'random_category_1_products': random_category_1_products,
            'random_category_2': random_category_2,
            'random_category_2_products': random_category_2_products,
            'hot_deals': hot_deals,
            'most_popular': most_popular,
            'category_hierarchy': category_hierarchy,
            }

        return Response(response_data, status=status.HTTP_200_OK)
    elif request.method == 'GET' and request.GET.get('query') == 'fetch_products_by_category':
        data = []
        category_name = 'All Products'
        category_id = request.GET.get('category_id')
        # if id is 0 fetch all products
        if category_id == '0':
            products = resource.fetch_all_products()
        else:
            products = resource.fetch_products_by_category(category_id)
            category = resource.fetch_product_category(category_id)
            category_name = category.name

        if products:
            serializer = ProductSerializer(products, many=True)
            data = serializer.data
        
        return Response({'products':data, 'category_name':category_name}, status=status.HTTP_200_OK)

    return render(request, 'products.html')

# route for adding a new product
@login_required(login_url='vendor_login')
@api_view(['GET','POST'])
def AddProductView(request):
    # get all product categories
    categories = resource.get_category_hierarchy()

    if request.method == 'POST':
        query = request.GET.get('query')
        if query == 'add_new_product':
            response = add_product(request)
            return response
        elif query == 'upload_product_photos':
            # get the product id
            product_id = request.POST.get('product_id')
            # get the product object
            product = get_product_object(product_id)
            # get the uploaded files
            files = request.FILES.getlist('product_images')

            # upload the images to cloudinary
            count = 0
            try:
                for file in files:
                    count += 1
                    cloud_pid = sanitize_string(f'{product.slug}_{count}')
                    sanitized_category_name = sanitize_string(product.category.name)
                    image_manager = ImageManager(file, sanitized_category_name, cloud_pid)
                    image_manager.upload_image()
                    #image_manager.optimize_image()
                    #image_manager.transform_image(200, 200)
                
                    # update the product object with the image URLs
                    setattr(product, f'image_{count}_cloud_url', image_manager.image_url)
                    setattr(product, f'image_{count}_cloud_thumb_url', image_manager.image_thumb_url)
                    setattr(product, f'image_{count}_pid', image_manager.image_public_id)
                    setattr(product, f'image_{count}_thumb_pid', image_manager.thumbnail_public_id)

                    # ensure max iteration is 4
                    if count == 4:
                        break
                
                product.save()
            except Exception as e:
                message = f"{e}"
                messages.error(request, message)
                return render(request, 'add_product.html', {'categories': categories}) #Response({"errors": message}, status=status.HTTP_400_BAD_REQUEST)
            
            messages.success(request, 'Product photos uploaded successfully.')
            return render(request, 'vendor_dashboard.html') #go to product list page

    return render(request, 'add_product.html', {'categories': categories})

# edit product route
@login_required(login_url='vendor_login')
@api_view(['GET','POST'])
def EditProductView(request):
    if request.method == 'GET':
        user = request.user
        product_id = request.GET.get('product_id')
        product = resource.fetch_vendor_product(user, product_id)
        categories = get_category_hierarchy()
        return render(request, 'edit_product.html', {'product': product, 'categories': categories})
    elif request.method == 'POST':
        query = request.GET.get('query')
        if query == 'update_product':
            data = request.data
            product_id = data.get('product_id')
            product = get_product_object(product_id)
            product_data = data.get('table_fields')
            product.name = product_data.get('product_name')
            product.stock = product_data.get('stock')
            product.description = product_data.get('description')
            product.product_feature = product_data.get('product_feature')
            product.cprice = float(product_data.get('cprice'))
            product.preprice = float(product_data.get('preprice'))
            product.min_quantity = product_data.get('min_quantity')
            product.buyer_notes = product_data.get('buyer_notes')
            product.last_updated_by = request.user.id
            product.save()
            messages.success(request, 'Product updated successfully.')
            return render(request, 'vendor_dashboard.html') #go to product list page
        
    #return render(request, 'edit_product.html')

# vendor products route
@login_required(login_url='vendor_login')
@api_view(['GET','POST','PUT','DELETE'])
def VendorProductsView(request):
    if request.method == 'GET':
        user = request.user
        products = Products.objects.filter(store=user)
    elif request.method == 'DELETE':
        request_data = request.data
        user = fetch_user(request_data.get('user_id'))
        if user.profile.user_type != 'vendor':
            return Response({'errors': 'You are not allowed to delete products.'}, status=status.HTTP_403_FORBIDDEN)
        # check if user is logged in
        if not user.is_authenticated:
            return Response({'errors': 'You are not allowed to delete products.'}, status=status.HTTP_403_FORBIDDEN)
        # get the product object
        product = resource.fetch_vendor_product(user, request_data.get('product_id'))
        if not product:
            return Response({'errors': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        # delete the product images from cloudinary
        for i in range(1, 5):
            image_pid = getattr(product, f'image_{i}_pid')
            thumb_pid = getattr(product, f'image_{i}_thumb_pid')
            if image_pid:
                cloudinary.uploader.destroy(image_pid)
            if thumb_pid:
                cloudinary.uploader.destroy(thumb_pid)
        # delete the product
        product.delete()
        message = 'Product deleted successfully.'
        messages.success(request, message)
        return Response({'success': message}, status=status.HTTP_200_OK)
    
    return render(request, 'vendor_products.html', {'products': products, 'store': user})

# route for search query
@api_view(['GET'])
def SearchView(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            # get all products that matches the search query fully or partially
            results = resource.search_products(query)
            if results:
                serializer = ProductSerializer(results, many=True)
                return Response({'products':serializer.data, 'query': query}, status=status.HTTP_200_OK)
        
    return Response({'products': []}, status=status.HTTP_200_OK)


def add_product(request):
    # get the parsed data from the request object
    data = request.data
    product_id = 0

    # get the user object
    user = get_user_object(data.get('user_id'))

    # check if user is vendor
    if user.profile.user_type != 'vendor':
        return Response({'errors': 'You are not allowed to add products.'}, status=status.HTTP_403_FORBIDDEN)
    
    # extract the product data from the request data
    product_data = data.get('table_fields')

    # get the category object
    category = ProductCategory.objects.get(id=product_data.get('category_id'))

    # delete all products from the database
    #Products.objects.all().delete()


    # create the product object
    try:
        product = Products.objects.create(
            store=user,
            category=category,
            name=product_data.get('product_name'),
            stock=product_data.get('stock'),
            description=product_data.get('description'),
            product_feature=json.dumps(product_data.get('product_feature')),
            cprice=float(product_data.get('cprice')),
            preprice=float(product_data.get('preprice')),
            min_quantity=product_data.get('min_quantity'),
            sizes=process_sizes(product_data),
            colors=process_colors(product_data),
            length=float(product_data.get('length')),
            width=float(product_data.get('width')),
            height=float(product_data.get('height')),
            weight=float(product_data.get('weight')),
            #vat=product_data.get('vat'),
            #product_brand=product_data.get('product_brand'),
            product_status='draft',
            buyer_notes=product_data.get('buyer_notes'),
            last_updated_by=user.id,
        )
        product_id = product.id
        product.save()
        message = 'Product added successfully.'
        messages.success(request, message)
    except Exception as e:
        message = f"{e}"
        messages.error(request, message)
        return Response({"errors": message}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"success": message, "product_id": product_id}, status=status.HTTP_201_CREATED)

def process_sizes(data):
    sizes = data.get('sizes')
    sizes = sizes.split(',')
    sizes = [size.strip() for size in sizes]
    if len(sizes) > 0:
        return sizes
    return None

def process_colors(data):
    colors = data.get('colors')
    colors = colors.split(',')
    colors = [color.strip() for color in colors]
    if len(colors) > 0:
        return colors
    return None