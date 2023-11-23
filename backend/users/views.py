import datetime
import logging

import jwt
from jwt import ExpiredSignatureError, DecodeError
from django.db.models import Q
import requests
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from users.serializer import MemberSerializer

from core import custom_errors, settings
from users.authorize import user_authorization
from users.models.members import Members
from users import user_errors

logger = logging.getLogger(__name__)


def generate_access_token(user_id):
    access_token_payload = {
        "id": user_id,
        "type": "access",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
    }
    return jwt.encode(access_token_payload, settings.SECRET_KEY, algorithm="HS256")


def generate_refresh_token(user_id):
    refresh_token_payload = {
        "id": user_id,
        "type": "refresh",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
    }
    return jwt.encode(refresh_token_payload, settings.SECRET_KEY, algorithm="HS256")


def verify_google_access_token(token):
    url = "https://www.googleapis.com/oauth2/v1/tokeninfo"
    params = {"access_token": token}

    try:
        response = requests.get(url, params=params)
        token_info = response.json()

        if "error_description" in token_info:
            return False
        else:
            return True
    except requests.RequestException:
        return False


def extract_user_info(token):
    is_valid = verify_google_access_token(token)
    url = "https://www.googleapis.com/oauth2/v1/userinfo"
    headers = {"Authorization": f"Bearer {token}"}
    if is_valid:

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                user_info = response.json()
                email = user_info.get("email")
                name = user_info.get("name")
                if email and name:
                    return email, name

        except requests.RequestException:
            return Response(
                {"error_code": 1006, "message": f"Request failed: {str()}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


def fetch_user_by_email(email):
    user = Members.objects.filter(Q(email=email )|Q(email=email.replace("com","org")) ).first()
    logger.info("user exists in db")
    return user
    # User with the given email does not exist


@api_view(["POST"])
@permission_classes([AllowAny])
def google_login(request):
    required_keys = ["access_token"]

    if not all(key in request.data for key in required_keys):
        return Response(
            custom_errors.MISSING_REQUIRED_FIELDS,
            status=status.HTTP_400_BAD_REQUEST,
        )

    access_token = request.data["access_token"]
    user_info = extract_user_info(access_token)

    if user_info is None:
        logger.error("Unable to extract user info from token")
        return Response(
            user_errors.TOKEN_ERROR,
            status=status.HTTP_400_BAD_REQUEST,
        )
    user_email, name = user_info[0], user_info[1]
    
    if user_email is None or name is None:
        return Response(
            user_errors.TOKEN_ERROR,
            status=status.HTTP_400_BAD_REQUEST,
        )
        
    user = Members.objects.filter(Q(email=user_email )|Q(email=user_email.replace("com","org")) ).first()
    if user is None:
        return Response(
            user_errors.UNAUTHORIZED_USER,
            status=status.HTTP_403_FORBIDDEN,
        )
    refresh = generate_refresh_token(user.id)
    access = generate_access_token(user.id)
    logger.info("Successfully generated access and refresh tokens")

    return Response(
        {"Refresh_Token": str(refresh), "Access_Token": str(
            access), "username": name},
        status=status.HTTP_200_OK,
    )


# api for genering accesstoken from refresh token
@api_view(["POST"])
@permission_classes([AllowAny])
def create_access_token_from_refresh_token(request):
    required_keys = ["refresh_token"]
    try:
        if not all(key in request.data for key in required_keys):
            logger.error("all fields are required")
            return Response(
                custom_errors.MISSING_REQUIRED_FIELDS,
                status=status.HTTP_400_BAD_REQUEST,
            )

        refresh_token = request.data["refresh_token"]

        # Decode the token
        payload = jwt.decode(
            refresh_token, settings.SECRET_KEY, algorithms=["HS256"])
        user_email = payload.get("id")
        refresh = generate_refresh_token(user_email)
        access = generate_access_token(user_email)
        logger.info("successfully generated access and refresh tokens")
        return Response(
            {
                "Refresh_Token": str(refresh),
                "Access_Token": str(access),
            },
            status=status.HTTP_200_OK,
        )
    except ExpiredSignatureError as e:
        logger.exception(e)
        return Response(user_errors.TOKEN_EXPIRED, status=status.HTTP_401_UNAUTHORIZED)
    except DecodeError:
        return Response(user_errors.INVALID_TOKEN, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.exception(e)
        return Response(
            {"error_code": 1009, "message": "Internal Server Error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(['GET'])
def get_all_users(request):
    logger.info("get all user api")
    users = Members.objects.all()
    serializer = MemberSerializer(users, many=True)
    logger.info("get all user api success")
    response_date = serializer.data
    return Response(response_date)


@api_view(['GET'])
def get_user_by_id(request):
    try:
        user_id = request.GET.get('userid')
        logger.info("get user by id api")
        users = Members.objects.filter(id=user_id).values()
        serializer = MemberSerializer(users, many=True)
        response_date = serializer.data
        return Response(response_date)
    except Exception:
        return Response({"error_code": 1009, "message": "Internal Server Error"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,)
