from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Appointment, Room, RoomReservation
from .serializers import AppointmentSerializer, RoomReservationSerializer, RoomSerializer
from datetime import datetime
from rest_framework.exceptions import ValidationError
from .validations import ScheduleValidator

class AppointmentCreateView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # check if times are valid
            ScheduleValidator().validate_appointment(
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

class AppointmentListInAPeriodView(APIView):
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
            end_ts__lte=end_ts,
            paciente__isnull=True,
        )

        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class AppointmentReservation(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        # Get query parameters
        appointment_id = request.query_params['appointment_id']
        paciente_id = request.query_params['paciente_id']
        
        if not appointment_id or not paciente_id:
            raise ValidationError("Both 'appointment_id' and 'paciente_id' must be provided.")
        
        appointment = Appointment.objects.get(id=appointment_id)
        if appointment.paciente is not None:
            raise ValidationError("Appointment already reserved by another patient.")
        
        Appointment.objects.filter(id=appointment_id).update(paciente=paciente_id)
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RoomManageView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    def delete(self, request):
        room_id = request.data.get('id')
        if not room_id:
            raise ValidationError("Room id must be provided.")
        room = Room.objects.get(id=room_id)
        room.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request):
        room_id = request.data.get('id')
        if not room_id:
            raise ValidationError("Room id must be provided.")
        room = Room.objects.get(id=room_id)
        serializer = RoomSerializer(room, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    def get(self, request):
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class RoomReservationManageView(APIView):
    permission_classes = (permissions.AllowAny,)

    def delete(self, request):

        room_reservation_id = request.query_params.get('id')
        if not room_reservation_id:
            raise ValidationError("Room reservation id must be provided.")
        room_reservation = RoomReservation.objects.get(id=room_reservation_id)
        room_reservation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request):

        doctor_id = request.query_params.get('medico')
        
        if not doctor_id:
            raise ValidationError("Doctor id must be provided.")
        
        #pegar todos os agendamentos do medico
        room_reservations = RoomReservation.objects.filter(medico=doctor_id)

        #serializar os agendamentos
        serializer = RoomReservationSerializer(room_reservations, many=True)

        #para cada agendamento, pegar o nome da sala e horário
        for room_reservation in serializer.data:
            room = Room.objects.get(id=room_reservation['room'])
            room_reservation['room_name'] = room.name

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        
        room = Room.objects.get(name=request.data.get('room_name'))
        serializer_data = {
            'room': room.id,
            'start_ts': request.data.get('start_ts'),
            'end_ts': request.data.get('end_ts'),
            'medico': request.data.get('medico'),
        }
        serializer = RoomReservationSerializer(data=serializer_data)
        if serializer.is_valid(raise_exception=True):
            
            # check if times are valid
            ScheduleValidator().validate_room_reservation(
               serializer.validated_data.get('start_ts'),
                serializer.validated_data.get('end_ts')
            )
            data = serializer.validated_data
            print(data)
            room = serializer.validated_data.get('room')
            room = Room.objects.get(id=room.id)

            # check for colisions:
            self.check_colisions(serializer.validated_data, room)
            
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def check_colisions(self, validated_data, room):

        start_ts = validated_data.get('start_ts')
        end_ts = validated_data.get('end_ts')

        if room and start_ts and end_ts:
            overlapping_appointments = RoomReservation.objects.filter(
                room=room,
                start_ts__lt=end_ts,
                end_ts__gt=start_ts
            )

            if overlapping_appointments.exists():
                raise ValidationError('Room already has another schedule overlapping with the proposed times.')