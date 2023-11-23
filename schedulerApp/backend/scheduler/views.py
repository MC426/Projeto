from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Appointment
from .serializers import AppointmentSerializer
from datetime import datetime
from rest_framework.exceptions import ValidationError

class AppointmentCreateView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_custom_validation(serializer.validated_data)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_custom_validation(self, validated_data):
        # Custom validation logic to check if medico has another schedule overlapping with proposed times
        medico = validated_data.get('medico')
        start_ts = validated_data.get('start_ts')
        end_ts = validated_data.get('end_ts')

        if medico and start_ts and end_ts:
            overlapping_appointments = Appointment.objects.filter(
                medico=medico,
                start_ts__lt=end_ts,
                end_ts__gt=start_ts
            )

            if overlapping_appointments.exists():
                raise ValidationError('Medico already has another schedule overlapping with the proposed times.')

class AppointmentListView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        # Get query parameters
        medico_id = request.query_params.get('medico_id')
        paciente_id = request.query_params.get('paciente_id')

        # Filter appointments based on query parameters
        if medico_id:
            appointments = Appointment.objects.filter(medico__user_id=medico_id)
        elif paciente_id:
            appointments = Appointment.objects.filter(paciente__user_id=paciente_id)
        else:
            raise ValidationError("Either 'medico_id' or 'paciente_id' must be provided.")

        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
