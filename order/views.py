import stripe

from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import status, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Order, OrderItem
from .serializers import OrderSerializer, MyOrderSerializer


class CheckoutAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Handles the checkout process, including creating a Stripe charge
        and saving the order data.
        """
        serializer = OrderSerializer(data=request.data)

        if serializer.is_valid():
            stripe.api_key = settings.STRIPE_SECRET_KEY
            paid_amount = sum(
                item.get('quantity') * item.get('product').price 
                for item in serializer.validated_data['items']
            )

            try:
                # Create a charge with Stripe
                charge = stripe.Charge.create(
                    amount=int(paid_amount * 100),  # Stripe requires amount in cents
                    currency='USD',
                    description='Charge from CodexZo Ecommerce',
                    source=serializer.validated_data['stripe_token']
                )

                # Save the order details
                serializer.save(
                    user=request.user, paid_amount=paid_amount
                )

                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
            except stripe.error.StripeError as e:
                # Handle Stripe error
                return Response(
                    {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
                )
            except Exception as e:
                # Handle other exceptions
                return Response(
                    {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
                )

        # If serializer is invalid, return errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class OrderListAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        orders = Order.objects.filter(user=request.user)
        serializer = MyOrderSerializer(orders, many=True)
        return Response(serializer.data)
