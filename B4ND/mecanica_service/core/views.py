from django.shortcuts import render
from rest_framework import viewsets, permissions, generics
from .models import MechanicProfile, Service, Booking, Payment
from django.contrib.auth.models import User
from .serializers import UserSerializer, MechanicProfileSerializer, ServiceSerializer, BookingSerializer, PaymentSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
import csv
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class MechanicProfileViewSet(viewsets.ModelViewSet):
    queryset = MechanicProfile.objects.all()
    serializer_class = MechanicProfileSerializer
    permission_classes = [IsAuthenticated]

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'user', 'service']

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

# Vista para descarga CSV filtrando bookings
from rest_framework.views import APIView

class BookingCSVDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        status_filter = request.GET.get('status', None)
        bookings = Booking.objects.all()
        if status_filter:
            bookings = bookings.filter(status=status_filter)
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="bookings.csv"'

        writer = csv.writer(response)
        writer.writerow(['id', 'user', 'service', 'date', 'status'])
        for b in bookings:
            writer.writerow([b.id, b.user.username, b.service.name, b.date, b.status])

        return response
