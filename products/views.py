from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category

# Create your views here.

def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    # define query and categories as none to avoid error on initial page loading
    query = None
    categories = None

    if request.GET:
        # check if category is in the GET request
        if 'category' in request.GET:
            # if exists, split into a list at the commas
            categories = request.GET['category'].split(',')
            # use list to fiter products to those only with the category name in their category lists
            products = products.filter(category__name__in=categories)
            # filter category models to show user what categories they have selected
            categories = Category.objects.filter(name__in=categories)

        # if there is data in the request under the form input name
        if 'q' in request.GET:
            # store the data as a variable
            query = request.GET['q']
            # if no data then display error message and redirect back to the products page
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            # generate search query object using Q object from Django
            # the i before contains makes queries case insensitive
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            # filter the items uing the query object
            products = products.filter(queries)

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)
    