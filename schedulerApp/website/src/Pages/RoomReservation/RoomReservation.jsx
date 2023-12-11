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
  const {createRoomReservation} = useUser();

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

  return (
    <div style={{ margin : '2%'}}>
      <h1>Suas reservas</h1>
      <h1>Salas disponíveis</h1>
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
          <h2>Reserva da sala {roomId} com início às {startDate} criada com sucesso</h2>
        </div>
      )}
      {formSubmitted && !reservationCreated && (
        <div style = {{marginTop :'5vh'}}>
          <h2>Erro ao criar reserva</h2>
        </div>
      )}
    </div>
  );
};

export default RoomReservation;