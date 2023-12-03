from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import *
from .models import *


@api_view(["GET"])
def search_audiences(request):
   
    query = request.GET.get("query", "")

    audiencess = Audiences.objects.filter(status=1).filter(number__icontains=query)

    serializer = AudiencesSerializer(audiencess, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_audiences_by_id(request, audiences_id):
    if not Audiences.objects.filter(pk=audiences_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    auditorium = Audiences.objects.get(pk=audiences_id)
    serializer = AudiencesSerializer(auditorium, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
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
def create_audiences(request):
    Audiences.objects.create()

    audiencess = Audiences.objects.all()
    serializer = AudiencesSerializer(audiencess, many=True)
    print(audiencess)
    print('--------------------------------------')
    print(serializer.data)
    return Response(serializer.data)


@api_view(["DELETE"])
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
def add_audiences_to_booking(request, audiences_id):
    if not Audiences.objects.filter(pk=audiences_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    print(12321)
    audiences = Audiences.objects.get(pk=audiences_id)
    print(audiences)
    booking = Booking.objects.filter(status=1).last()
    print(booking)
    if booking is None:
        booking = Booking.objects.create()
    # audiencess = Audiences.objects.filter(status=1)
    booking.audincess.add(audiences)
    # booking.audiences.add(audiences)
    booking.save()

    serializer = AudiencesSerializer(booking.audincess, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_audiences_image(request, audiences_id):
    if not Audiences.objects.filter(pk=audiences_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    pioneer = Audiences.objects.get(pk=audiences_id)

    return HttpResponse(pioneer.image, content_type="image/png")


@api_view(["PUT"])
def update_audiences_image(request, audiences_id):
    if not Audiences.objects.filter(pk=audiences_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    pioneer = Audiences.objects.get(pk=audiences_id)
    serializer = AudiencesSerializer(pioneer, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["GET"])
def get_booking(request):
    bookings = Booking.objects.all()
    serializer = BookingSerializer(bookings, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_booking_by_id(request, booking_id):
    if not Booking.objects.filter(pk=booking_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    discovery = Booking.objects.get(pk=booking_id)
    serializer = BookingSerializer(discovery, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
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
def delete_booking(request, booking_id):
    if not Booking.objects.filter(pk=booking_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    bookings = Booking.objects.get(pk=booking_id)
    bookings.status = 5
    bookings.save()

    return Response(status=status.HTTP_200_OK)


@api_view(["DELETE"])
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

