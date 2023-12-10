import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { confirmAlert } from 'react-confirm-alert';
import 'react-confirm-alert/src/react-confirm-alert.css';
import './RoomReservation.css';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

const client = axios.create({
  baseURL: "http://localhost:8000"
});

// todo: realmente fazer uma chamada para o backend para criar o agendamento
const ListAvailableTimes = () => {
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [appointments, setAppointments] = useState([]);
  const [formSubmitted, setFormSubmitted] = useState(false);

  const formatDate = (dateString) => {
    const options = {
        day: 'numeric',
        month: 'numeric',
        year: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        timeZone: 'UTC', // Deixa esse timezone porque eh o usado em todo lugar
      };
      return new Date(dateString).toLocaleString('pt-BR', options);
    };


  const handleSubmit = (e) => {
    e.preventDefault();
    const fetchAppointments = async () => {
        try {
          const response = await 
          client.get("/api/scheduler/list-in-period", { withCredentials: true,
              params: { start_ts: startDate, end_ts: endDate }
          }).then(response => {
              setAppointments(response.data);
              console.log("Consegui os dados: ", response.data);
          })
          .catch(error => {
              console.error("Error fetching schedules:", error); 
          });
        } catch (error) {
          console.error('Error fetching appointments:', error);
        }
      };
  
    fetchAppointments();
    setFormSubmitted(true);
  };

  const handleAppointmentButtonClick = (appointment) => {
    confirmAlert({
      title: 'Appointment Details',
      message: `Horario: ${formatDate(appointment.start_ts)} até ${formatDate(appointment.end_ts)}.\n`
        + `Medico: ${appointment.user_id}.\n`
        + `Localizacao: Rua Joaquim Joao 123.`
        ,
      buttons: [
        {
          label: 'OK',
          // todo: realmente fazer uma chamada para o backend para criar o agendamento
          onClick: () => console.log('User clicked OK'),
        },
      ],
    });
  };


  return (
    <div style={{ margin : '2%'}}>
      <h1>Consultar Horários</h1>
      <form onSubmit={handleSubmit}>
        <div className = "Dates">
          <strong>Data de Inicio:    </strong>    
          <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} />
        </div>

        <div className = "Dates">
          <strong>Data de Término:    </strong>    
          <input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} />
        </div>
        <button type="submit">Consultar</button>
      </form>
      {formSubmitted && (
        <div style = {{marginTop :'5vh'}}>
          <h2>Consultas:</h2>
          <div style = {{ marginTop :'2vh'}}>
            {appointments.map((appointment) => (
              <button
                key={appointment.id}
                onClick={() => handleAppointmentButtonClick(appointment)}
                style = {{  margin: '1.5vh', padding: '1.5vh',}}
              >
                <strong>{"Horario: "}</strong>
                {formatDate(appointment.start_ts)} até {formatDate(appointment.end_ts)}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ListAvailableTimes;