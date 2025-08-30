from django.urls import path, include

from product import views

urlpatterns = [
    path(
        'latest-products/',
        views.LatestProductsList.as_view(),
        name='latest-products'
    ),
    path(
        'products/<slug:category_slug>/<slug:product_slug>/',
        views.ProductDetail.as_view(),
        name='product-detail'
    ),
    path(
        'category/<slug:category_slug>/',
        views.CategoryDetail.as_view(),
        name='category-detail'
    ),
    path(
        'products/search/',
        views.ProductSearchView.as_view(),
        name='product-search'
    ),
]
