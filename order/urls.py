from django.urls import path

from order import views

urlpatterns = [
    path(
        'checkout/',
        views.CheckoutAPIView.as_view(),
        name='checkout'
    ),
    path(
        'my-orders/',
        views.OrderListAPIView.as_view(),
        name='my-orders'
    ),
]
