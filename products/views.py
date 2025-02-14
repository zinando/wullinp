from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from _core.utils.helpers import get_category_hierarchy, get_user_object, get_product_object, sanitize_string
from _core.image_manager import ImageManager
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Products, ProductCategory
from django.contrib import messages
from .model_serializer import ProductSerializer

# Create your views here.
#@login_required(login_url='/user/login/')
@api_view(['GET'])
def ProductView(request):
    """This view renders the products page."""
    if request.method == 'GET' and request.GET.get('query') == 'fetch_public_products':

        # get all products
        products = Products.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    return render(request, 'products.html')

@login_required(login_url='vendor_login')
@api_view(['GET','POST'])
def AddProductView(request):
    # get all product categories
    categories = get_category_hierarchy()

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
            product_feature=product_data.get('product_feature'),
            cprice=float(product_data.get('cprice')),
            preprice=float(product_data.get('preprice')),
            min_quantity=product_data.get('min_quantity'),
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


