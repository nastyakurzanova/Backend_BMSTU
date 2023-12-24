import requests
from django.conf import settings
from django.contrib.auth import authenticate
from django.core.cache import cache
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .jwt_helper import create_access_token, create_access_token, get_jwt_payload
from .permissions import *
from .serializer import *


access_token_lifetime = settings.JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()
# 5 лаба htubcnhfwbz
@api_view(["POST"])
def register(request):
    serializer = UserRegisterSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(status=status.HTTP_409_CONFLICT)

    user = serializer.save()

    access_token = create_access_token(user.id)

    user_data = {
        "user_id": user.id,
        "name": user.name,
        "email": user.email,
        "is_moderator": user.is_moderator,
        "access_token": access_token
    }

    cache.set(access_token, user_data, access_token_lifetime)

    message = {
        'message': 'User registered successfully',
        'user_id': user.id,
        "access_token": access_token
    }

    response = Response(message, status=status.HTTP_201_CREATED)

    response.set_cookie('access_token', access_token, httponly=False, expires=access_token_lifetime)

    return response


@api_view(["POST"])
def login(request):
    serializer = UserLoginSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(**serializer.data)
    if user is None:
        message = {"message": "invalid credentials"}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)

    access_token = create_access_token(user.id)

    user_data = {
        "user_id": user.id,
        "name": user.name,
        "email": user.email,
        "is_moderator": user.is_moderator,
        "access_token": access_token,
    }
    cache.set(access_token, user_data, access_token_lifetime)

    response = Response(user_data, status=status.HTTP_201_CREATED)

    response.set_cookie('access_token', access_token, httponly=True, expires=access_token_lifetime)

    return response

@api_view(["POST"])
def check(request):
    access_token = get_access_token(request)

    if access_token is None:
        message = {"message": "Token is not found"}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)

    if not cache.has_key(access_token):
        message = {"message": "Token is not valid"}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)

    user_data = cache.get(access_token)

    return Response(user_data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    access_token = get_access_token(request)

    #  Check access token is in Redis
    if cache.has_key(access_token):
        # Delete access token from Redis
        cache.delete(access_token)

    # Create response object
    message = {"message": "Logged out successfully!"}
    response = Response(message, status=status.HTTP_200_OK)

    # Delete access token from cookie
    response.delete_cookie('access_token')

    return response

# 3 лаба функции!!!!!!!!!!!!!!1


def get_draft_audiences():
    # audiences = Audiences.objects.filter(status=1).first()
    audiences = Audiences.objects.filter(status=1).first()
    if audiences is None:
        return None

    return audiences


@api_view(["GET"])
def search_audiences(request):
    name = request.GET.get('query', '')
    
    audiences = Audiences.objects.filter(status=1).filter(name__contains=name)
    
    serializer = AudiencesSerializer(audiences, many=True)
    draft_audiences = get_draft_audiences()
    # draft_audiences.pk
    data = {
        "info": serializer.data,
        "draft_audiences": draft_audiences.pk if draft_audiences else None
    }
    print(data)
    return Response(data)

@api_view(["GET"])
def get_audiences_by_id(request, audiences_id):
    if not Audiences.objects.filter(pk=audiences_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    auditorium = Audiences.objects.get(pk=audiences_id)
    serializer = AudiencesSerializer(auditorium, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsModerator])
def update_audiences(request, audiences_id):
    if not Audiences.objects.filter(pk=audiences_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    auditorium = Audiences.objects.get(pk=audiences_id)
    serializer = AudiencesSerializer(auditorium, data=request.data, many=False, partial=True)
    print(serializer.is_valid())
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsModerator])
def create_audiences(request):
    Audiences.objects.create()
    # serializer = AudiencesSerializer(data=request.data)
    # serializer.initial_data["image"] = request.FILES['image']
    # if(serializer.is_valid()):
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    audiences = Audiences.objects.all()
    serializer = AudiencesSerializer(audiences, many=True)

    return Response(serializer.data)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_audiences(request, audiences_id):
    if not Audiences.objects.filter(pk=audiences_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    auditorium = Audiences.objects.get(pk=audiences_id)
    auditorium.status = 2
    auditorium.save()

    audiencess = Audiences.objects.filter(status=1)
    serializer = AudiencesSerializer(audiencess, many=True)

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_audiences_to_booking(request, audiences_id):
    access_token = get_access_token(request)
    payload = get_jwt_payload(access_token)
    user_id = payload["user_id"]
    if not Audiences.objects.filter(pk=audiences_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    audiences = Audiences.objects.get(pk=audiences_id)
    print(audiences)
    
    booking = Booking.objects.filter(status=1).filter(user_id=user_id).last()
    print(booking)
    
    if booking is None:
        booking = Booking.objects.create()
    # audiencess = Audiences.objects.filter(status=1)
    booking.audiences.add(audiences)
    # booking.audiences.add(audiences)
    booking.user = CustomUser.objects.get(pk=user_id)
    booking.save()

    serializer = AudiencesSerializer(booking.audiences, many=True)

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_audiences_image(request, audiences_id):
    if not Audiences.objects.filter(pk=audiences_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    audiences = Audiences.objects.get(pk=audiences_id)

    return HttpResponse(audiences.image, content_type="image/png")


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_audiences_image(request, audiences_id):
    if not Audiences.objects.filter(pk=audiences_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    pioneer = Audiences.objects.get(pk=audiences_id)
    serializer = AudiencesSerializer(pioneer, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

# @api_view(["GET"])
# def search_cosmetics(request):
#     cosmetics = Cosmetic.objects.all()

#     request_status = request.GET.get("status")
#     if request_status:
#         cosmetics = cosmetics.filter(status=request_status)

#     serializer = CosmeticSerializer(cosmetics, many=True)

#     return Response(serializer.data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_booking(request):
    token = get_access_token(request)
    payload = get_jwt_payload(token)
    user_id = payload["user_id"]
    bookings = Booking.objects.filter(user_id=user_id)
    serializer = BookingSerializer(bookings, many=True)

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_booking_by_id(request, booking_id):
    if not Booking.objects.filter(pk=booking_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    booking = Booking.objects.get(pk=booking_id)
    serializer = BookingSerializer(booking, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_booking(request, booking_id):
    if not Booking.objects.filter(pk=booking_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    bookings = Booking.objects.get(pk=booking_id)
    serializer = BookingSerializer(bookings, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    bookings.status = 1
    bookings.save()

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_status_user(request, booking_id):
    if not Booking.objects.filter(pk=booking_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    request_status = request.data["status"]

    if request_status not in [1, 5]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    bookings = Booking.objects.get(pk=booking_id)
    lesson_status = bookings.status

    if lesson_status == 5:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    bookings.status = request_status
    bookings.save()

    serializer = BookingSerializer(bookings, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsModerator])
def update_status_admin(request, booking_id):
    if not Booking.objects.filter(pk=booking_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    request_status = request.data["status"]

    if request_status in [1, 5]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    bookings = Booking.objects.get(pk=booking_id)

    lesson_status = bookings.status

    if lesson_status in [3, 4, 5]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    bookings.status = request_status
    bookings.save()

    serializer = BookingSerializer(bookings, many=False)

    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_booking(request, booking_id):
    if not Booking.objects.filter(pk=booking_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    bookings = Booking.objects.get(pk=booking_id)
    bookings.status = 5
    bookings.save()

    return Response(status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_audiences_from_booking(request, booking_id, audiences_id):
    if not Booking.objects.filter(pk=booking_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not Audiences.objects.filter(pk=audiences_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    bookings = Booking.objects.get(pk=booking_id)
    bookings.audincess.remove(Audiences.objects.get(pk=audiences_id))
    bookings.save()

    serializer = AudiencesSerializer(bookings.audincess, many=True)

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_free_audiences(request, booking_id):
    if not Booking.objects.filter(pk=booking_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    print(f'========== {request.data}')
    # if(request.data[0]==1234567890):
    #     print("123321")
    element_value = request.data.get('access_token', 0)
    if(element_value==1234567890):
        booking = Booking.objects.get(pk=booking_id)
        serializer = BookingSerializer(booking, data=request.data, many=False, partial=True)
        if serializer.is_valid():
            serializer.save()
        booking.save()
        print(booking.free_audiences)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


















# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11/
# !!! разобрать !!!
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_draft_order(request):
    token = get_access_token(request)
    payload = get_jwt_payload(token)
    user_id = payload["user_id"]

    order = Booking.objects.filter(owner_id=user_id).filter(status=1).first()

    if order is None:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = BookingSerializer(order, many=False)
    return Response(serializer.data)

# !!!
@api_view(["PUT"])
@permission_classes([IsRemoteWebService])
def update_order_delivery_date(request, pk):
    if not Booking.objects.filter(pk=pk).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    order = Booking.objects.get(pk=pk)

    days = request.data.get("delivery_date", -1)
    if days > 0:
        order.delivery_date = days
        order.save()
        return Response(status=status.HTTP_200_OK)

    return Response(status=status.HTTP_404_NOT_FOUND)



# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# @api_view(["GET"])
# def search_spares(request):
#     query = request.GET.get("query", "")
#     offset = int(request.GET.get("offset", 0))
#     limit = int(request.GET.get("limit", 5))

#     spares = Spare.objects.filter(name__icontains=query).filter(status=1)

#     serializer = SpareSerializer(spares[offset:offset + limit], many=True)

#     data = {
#         "spares": serializer.data,
#         "totalCount": len(spares)
#     }

#     return Response(data)


# @api_view(["GET"])
# def get_spare(request, pk):
#     if not Spare.objects.filter(pk=pk).exists():
#         return Response(f"Авизапчасти с таким id не существует!")

#     spare = Spare.objects.get(pk=pk)
#     serializer = SpareSerializer(spare, many=False)

#     return Response(serializer.data)


# @api_view(["GET"])
# def get_spare_image(request, pk):
#     if not Spare.objects.filter(pk=pk).exists():
#         return Response(f"Авизапчасти с таким id не существует!")

#     spare = Spare.objects.get(pk=pk)

#     return HttpResponse(spare.image, content_type="image/png")


# @api_view(["PUT"])
# @permission_classes([IsModerator])
# def update_spare(request, pk):
#     if not Spare.objects.filter(pk=pk).exists():
#         return Response(f"Авизапчасти с таким id не существует!")

#     spare = Spare.objects.get(pk=pk)
#     serializer = SpareSerializer(spare, data=request.data, many=False, partial=True)

#     if serializer.is_valid():
#         serializer.save()

#     return Response(serializer.data)


# @api_view(["POST"])
# @permission_classes([IsModerator])
# def create_spare(request):
#     spare = Spare.objects.create()

#     serializer = SpareSerializer(spare, many=False)
#     return Response(serializer.data)


# @api_view(["DELETE"])
# @permission_classes([IsModerator])
# def delete_spare(request, pk):
#     if not Spare.objects.filter(pk=pk).exists():
#         return Response(f"Авиазапчасти с таким id не существует!")

#     spare = Spare.objects.get(pk=pk)
#     spare.status = 2
#     spare.save()

#     spares = Spare.objects.filter(status=1)
#     serializer = SpareSerializer(spares, many=True)
#     return Response(serializer.data)


# @api_view(["POST"])
# @permission_classes([IsAuthenticated])
# def add_spare_to_order(request, spare_id):
#     access_token = get_access_token(request)
#     payload = get_jwt_payload(access_token)
#     user_id = payload["user_id"]

#     spare = Spare.objects.get(pk=spare_id)

#     order = Order.objects.filter(status=1).filter(owner_id=user_id).last()

#     if order is None:
#         order = Order.objects.create()

#     if order.spares.contains(spare):
#         return Response(status=status.HTTP_409_CONFLICT)

#     order.spares.add(spare)
#     order.owner = CustomUser.objects.get(pk=user_id)
#     order.save()

#     serializer = OrderSerializer(order, many=False)

#     response = Response()
#     response.data = serializer.data
#     response.status_code = status.HTTP_200_OK

#     return response


# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def search_orders(request):
#     token = get_access_token(request)
#     payload = get_jwt_payload(token)
#     user_id = payload["user_id"]
#     user = CustomUser.objects.get(pk=user_id)

#     offset = int(request.GET.get("offset", 0))
#     limit = int(request.GET.get("limit", 5))
#     status = int(request.GET.get("status", -1))

#     orders = Order.objects.exclude(status__in=[1, 5])

#     if not user.is_moderator:
#         orders = orders.filter(owner_id=user.pk)

#     if status != -1:
#         orders = orders.filter(status=status)

#     serializer = OrderSerializer(orders, many=True)

#     resp = {
#         "orders": serializer.data[offset:offset + limit],
#         "totalCount": len(serializer.data)
#     }

#     return Response(resp)


# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def get_draft_order(request):
#     token = get_access_token(request)
#     payload = get_jwt_payload(token)
#     user_id = payload["user_id"]

#     order = Order.objects.filter(owner_id=user_id).filter(status=1).first()

#     if order is None:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     serializer = OrderSerializer(order, many=False)
#     return Response(serializer.data)


# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def get_order(request, pk):
#     if not Order.objects.filter(pk=pk).exists():
#         return Response(f"Заказа с таким id не существует!")

#     order = Order.objects.get(pk=pk)
#     serializer = OrderSerializer(order, many=False)

#     return Response(serializer.data)


# @api_view(["PUT"])
# @permission_classes([IsAuthenticated])
# def update_order(request, pk):
#     if not Order.objects.filter(pk=pk).exists():
#         return Response(f"Заказа с таким id не существует!")

#     order = Order.objects.get(pk=pk)
#     serializer = OrderSerializer(order, data=request.data, many=False, partial=True)

#     if serializer.is_valid():
#         serializer.save()

#     return Response(serializer.data)


# @api_view(["PUT"])
# @permission_classes([IsRemoteWebService])
# def update_order_delivery_date(request, pk):
#     if not Order.objects.filter(pk=pk).exists():
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     order = Order.objects.get(pk=pk)

#     days = request.data.get("delivery_date", -1)
#     if days > 0:
#         order.delivery_date = days
#         order.save()
#         return Response(status=status.HTTP_200_OK)

#     return Response(status=status.HTTP_404_NOT_FOUND)


# def calculate_order_delivery_date(order_id):
#     data = {
#         "order_id": order_id,
#         "access_token": settings.REMOTE_WEB_SERVICE_AUTH_TOKEN,
#     }

#     requests.post("http://127.0.0.1:8080/calc_delivery_date/", json=data, timeout=3)


# @api_view(["PUT"])
# @permission_classes([IsAuthenticated])
# def update_order_user(request, pk):
#     if not Order.objects.filter(pk=pk).exists():
#         return Response(f"Заказа с таким id не существует!")

#     order = Order.objects.get(pk=pk)
#     order.status = 2
#     order.date_of_formation = timezone.now()
#     order.save()

#     calculate_order_delivery_date(order.pk)

#     serializer = OrderSerializer(order, many=False)

#     return Response(serializer.data, status=status.HTTP_200_OK)


# @api_view(["PUT"])
# @permission_classes([IsModerator])
# def update_order_admin(request, pk):
#     access_token = get_access_token(request)
#     payload = get_jwt_payload(access_token)
#     user_id = payload["user_id"]

#     if not Order.objects.filter(pk=pk).exists():
#         return Response(f"Заказа с таким id не существует!")

#     request_status = int(request.data["status"])

#     if request_status not in [3, 4]:
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

#     order = Order.objects.get(pk=pk)
#     order_status = order.status

#     if order_status != 2:
#         return Response("Статус изменить нельзя", status=status.HTTP_405_METHOD_NOT_ALLOWED)

#     order.status = request_status
#     order.date_complete = timezone.now()
#     order.moderator = CustomUser.objects.get(pk=user_id)
#     order.save()

#     serializer = OrderSerializer(order, many=False)

#     return Response(serializer.data)


# @api_view(["DELETE"])
# @permission_classes([IsAuthenticated])
# def delete_order(request, pk):
#     if not Order.objects.filter(pk=pk).exists():
#         return Response(f"Заказа с таким id не существует!")

#     order = Order.objects.get(pk=pk)
#     order.status = 5
#     order.save()

#     serializer = OrderSerializer(order, many=False)

#     return Response(serializer.data)


# @api_view(["DELETE"])
# @permission_classes([IsAuthenticated])
# def delete_spare_from_order(request, order_id, spare_id):
#     if not Order.objects.filter(pk=order_id).exists():
#         return Response(f"Заказа с таким id не существует")

#     if not Spare.objects.filter(pk=spare_id).exists():
#         return Response(f"Авиазапчасти с таким id не существует")

#     order = Order.objects.get(pk=order_id)
#     order.spares.remove(Spare.objects.get(pk=spare_id))
#     order.save()

#     serializer = OrderSerializer(order, many=False)

#     return Response(serializer.data)


# access_token_lifetime = settings.JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()


# @api_view(["POST"])
# def login(request):
#     # Ensure email and passwords are posted properly
#     serializer = UserLoginSerializer(data=request.data)

#     if not serializer.is_valid():
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     # Check credentials
#     user = authenticate(**serializer.data)
#     if user is None:
#         message = {"message": "invalid credentials"}
#         return Response(message, status=status.HTTP_401_UNAUTHORIZED)

#     # Create new access and refresh token
#     access_token = create_access_token(user.id)

#     # Add access token to redis for validating by other services
#     user_data = {
#         "user_id": user.id,
#         "name": user.name,
#         "email": user.email,
#         "is_moderator": user.is_moderator,
#         "access_token": access_token,
#     }
#     cache.set(access_token, user_data, access_token_lifetime)

#     # Create response object
#     response = Response(user_data, status=status.HTTP_201_CREATED)
#     # Set access token in cookie
#     response.set_cookie('access_token', access_token, httponly=True, expires=access_token_lifetime)

#     return response


# @api_view(["POST"])
# def register(request):
#     serializer = UserRegisterSerializer(data=request.data)

#     if not serializer.is_valid():
#         return Response(status=status.HTTP_409_CONFLICT)

#     user = serializer.save()

#     access_token = create_access_token(user.id)

#     user_data = {
#         "user_id": user.id,
#         "name": user.name,
#         "email": user.email,
#         "is_moderator": user.is_moderator,
#         "access_token": access_token
#     }

#     cache.set(access_token, user_data, access_token_lifetime)

#     message = {
#         'message': 'User registered successfully',
#         'user_id': user.id,
#         "access_token": access_token
#     }

#     response = Response(message, status=status.HTTP_201_CREATED)

#     response.set_cookie('access_token', access_token, httponly=False, expires=access_token_lifetime)

#     return response


# @api_view(["POST"])
# def check(request):
#     access_token = get_access_token(request)

#     if access_token is None:
#         message = {"message": "Token is not found"}
#         return Response(message, status=status.HTTP_401_UNAUTHORIZED)

#     if not cache.has_key(access_token):
#         message = {"message": "Token is not valid"}
#         return Response(message, status=status.HTTP_401_UNAUTHORIZED)

#     user_data = cache.get(access_token)

#     return Response(user_data, status=status.HTTP_200_OK)


# @api_view(["POST"])
# @permission_classes([IsAuthenticated])
# def logout(request):
#     access_token = get_access_token(request)

#     #  Check access token is in Redis
#     if cache.has_key(access_token):
#         # Delete access token from Redis
#         cache.delete(access_token)

#     # Create response object
#     message = {"message": "Logged out successfully!"}
#     response = Response(message, status=status.HTTP_200_OK)

#     # Delete access token from cookie
#     response.delete_cookie('access_token')

#     return response