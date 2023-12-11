import React, { useState, useEffect } from 'react';
import { confirmAlert } from 'react-confirm-alert';
import 'react-confirm-alert/src/react-confirm-alert.css';
import './RoomReservation.css';
import { useUser } from '../../backendFacade';

const RoomReservation = () => {
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [reservationCreated, setReservationCreated] = useState(false);
  const [formSubmitted, setFormSubmitted] = useState(false);
  const [roomId, setRoomId] = useState('');
  const {createRoomReservation, getRoomReservations, userData, getRooms, deleteReservation} = useUser();
  const [reservations, setReservations] = useState([]);
  const [rooms, setRooms] = useState([]);

  useEffect(() => {
    console.log("get user reservations with data", userData)
    getRoomReservations(userData.user_id)
    .then(response => setReservations(response.data))

    getRooms().then(response => setRooms(response.data))

  }, [reservationCreated]);

  const handleSubmit = (e) => {
    e.preventDefault();
    createRoomReservation(
      roomId,
      startDate,
      endDate).then((response) => {
        console.log("response create room reservation", response.data)
        setFormSubmitted(true);
        setReservationCreated(true);
      }).catch((error) => {
        console.log("error create room reservation", error)
        setFormSubmitted(true);
        setReservationCreated(false);
      });
  };

  const formatDate = (dateString) => {
    const [date, time] = dateString.split('T');
    const [year, month, day] = date.split('-');
    const [hour, minute] = time.split(':');
  
    return `${day}/${month}/${year}, ${hour}:${minute}`;
  };

  const handleDeleteButton = (reservationId) => () => {
    deleteReservation(reservationId).then(() => {
      getRoomReservations(userData.user_id)
      .then(response => setReservations(response.data))
    })
  }

  return (
    <div style={{ margin : '2%'}}>
      <h1>Suas reservas</h1>
      <div style={{ margin : '2%'}}>
        <ul>
          {reservations.length == 0 ?
          <p>Você ainda não possui reservas. As reservas que realizar com o formulário abaixo aparecerão aqui.</p>
          : (
            reservations.map((reservation) => {
              console.log("reservation", reservation)
              return (
                <li style={{margin: '1%'}}>
                  Reserva da sala {reservation.room_name} com início em {formatDate(reservation.start_ts)} e fim em {formatDate(reservation.end_ts)}
                  <button onClick={handleDeleteButton(reservation.id)} style={{marginLeft: '1%'}}>Cancelar reserva</button>
                </li>
            )
            })
          )}
        </ul>
      </div>
      <h1>Salas disponíveis para reserva</h1>
      <div style={{ margin : '2%'}}>
        <ul>
          {
            rooms.map((room) => {
              return (
                <li style={{margin: '1%'}}>
                  Sala {room.name}
                </li>
            )
            })
          }
        </ul>
      </div>
      <h1>Reservar sala</h1>
      <form onSubmit={handleSubmit}>
        <div className="InputDiv">
          <strong>Nome da sala:    </strong>
          <input type="text" value={roomId} onChange={(e) => setRoomId(e.target.value)} />
        </div>
        <div className = "InputDiv">
          <strong>Data de Inicio:    </strong>    
          <input type="datetime-local" value={startDate} onChange={(e) => setStartDate(e.target.value)} />
        </div>

        <div className = "InputDiv">
          <strong>Data de Término:    </strong>    
          <input type="datetime-local" value={endDate} onChange={(e) => setEndDate(e.target.value)} />
        </div>
        <button type="submit">Gerar reserva</button>
      </form>
      {formSubmitted && reservationCreated && (
        <div style = {{marginTop :'5vh'}}>
          <p style={{color: 'green'}}>Reserva da sala {roomId} com início às {formatDate(startDate)} criada com sucesso</p>
        </div>
      )}
      {formSubmitted && !reservationCreated && (
        <div style = {{marginTop :'5vh'}}>
          <p style={{color: 'red'}}>Erro ao criar reserva</p>
        </div>
      )}
    </div>
  );
};

export default RoomReservation;