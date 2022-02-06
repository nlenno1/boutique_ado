from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from django.contrib.auth.decorators import login_required

from .models import Product, Category
from .forms import ProductForm


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    # define query and categories as none to avoid error on initial page loading
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        # check if sort and diection are in the GET request
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

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

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)

@login_required
def add_product(request):
    """ Add a product to the store"""
    if not request.user.is_superuser:
        messages.error(request, "Sorry, only store owners can do that!")
        return redirect(reverse('home'))
    
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, "Sucessfully added product!")
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, "Failed to add product. Please ensure the\
                 form is valid.")
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)

@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, "Sorry, only store owners can do that!")
        return redirect(reverse('home'))
    
    product = get_object_or_404(Product, pk=product_id)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sucessfully Updated Product')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, "Failed to edit product. Please ensure the\
                form is valid.")
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product
    }

    return render(request, template, context)

@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, "Sorry, only store owners can do that!")
        return redirect(reveres('home'))
    
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, "Product has been deleted!")
    return redirect(reverse('products'))