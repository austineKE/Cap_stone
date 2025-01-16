from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.views import TokenObtainPairView


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.username
        print(self.user.username)
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

def get_username_from_jwt(token):
    try:
        # Decode the token
        decoded_payload = UntypedToken(token)
        return decoded_payload.get("user_id")  # Extract the username
    except (InvalidToken, TokenError) as e:
        print(f"Invalid token: {e}")
        return None


