from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]  # Allow login without authentication

    def post(self, request, *args, **kwargs):
        # Extract username and password from the request body
        username = request.data.get('username')
        password = request.data.get('password')
        
        # Authenticate the user manually using the credentials
        user = authenticate(username=username, password=password)
        
        # If authentication fails, raise an error
        if user is None:
            raise AuthenticationFailed("Invalid username or password")
        
        # Set the user on the request
        request.user = user

        # Call the default TokenObtainPairView logic to get the token
        response = super().post(request, *args, **kwargs)

        # Add user details to the response if the user is authenticated
        if request.user.is_authenticated:
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email if user.email else '',
                'first_name': user.first_name if user.first_name else '',
                'last_name': user.last_name if user.last_name else ''
            }
            # Add user details to the response
            response.data.update(user_data)

        return response
