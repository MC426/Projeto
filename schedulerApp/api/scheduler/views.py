from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Appointment
from .serializers import AppointmentSerializer, RoomSerializer
from datetime import datetime
from rest_framework.exceptions import ValidationError
from .validations import AppointmentValidator

class AppointmentCreateView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # check if times are valid
            AppointmentValidator().validate(
               serializer.validated_data.get('start_ts'),
                serializer.validated_data.get('end_ts')
            )
            # check for colisions:
            self.perform_custom_validation(serializer.validated_data)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_custom_validation(self, validated_data):
        # Custom validation logic to check if medico has another schedule overlapping with proposed times
        medico = validated_data.get('medico')
        start_ts = validated_data.get('start_ts')
        end_ts = validated_data.get('end_ts')
        if not start_ts or not end_ts:
            raise ValidationError('Both start_ts and end_ts must be provided.')

        if start_ts > end_ts:
            raise ValidationError('start_ts must be less than end_ts.')

        if not medico:
            raise ValidationError('Medico must be provided.')

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
        
        if not medico_id and not paciente_id:
            raise ValidationError("Either 'medico_id' or 'paciente_id' must be provided.")

        # Filter appointments based on query parameters
        if medico_id:
            appointments = Appointment.objects.filter(medico__user_id=medico_id)
        elif paciente_id:
            appointments = Appointment.objects.filter(paciente__user_id=paciente_id)

        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ApointmentListInAPeriodView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        # Get query parameters
        start_ts = request.query_params.get('start_ts')
        end_ts = request.query_params.get('end_ts')
        

        if not start_ts or not end_ts:
            raise ValidationError("Both 'start_ts' and 'end_ts' must be provided.")

        # Filter appointments based on query parameters
        appointments = Appointment.objects.filter(
            start_ts__gte=start_ts,
            end_ts__lte=end_ts
        )

        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class RoomCreateView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)