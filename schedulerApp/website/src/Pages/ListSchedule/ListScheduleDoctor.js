import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Calendar from 'react-calendar'; // Example calendar library, you can choose the one that fits your needs
import 'react-datetime/css/react-datetime.css';
import './ListSchedule.css';
import { useUser } from '../../backendFacade';
import { confirmAlert } from 'react-confirm-alert';
import '../Middle.css'

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

const ScheduleList = () => {
  const { userData, getUser, getUserById, deleteAppointment, listAppointmentMedico } = useUser();
  const [schedules, setSchedules] = useState([]);
  const [loading, setLoading] = useState(true);
  const [closestEventDate, setClosestEventDate] = useState(null);

  var user_id = null;

  useEffect(() => {
    // Calculate the closest event date when schedules change
    if (schedules.length > 0) {
      const closestDate = new Date(Math.min(...schedules.map(schedule => new Date(schedule.start_ts))));
      setClosestEventDate(closestDate);
    }
  }, [schedules]);


  const tileContent = ({ date, view }) => {
    if (view === 'month') {
      const dateWithoutTime = new Date(date.getFullYear(), date.getMonth(), date.getDate());
      const hasEvent = schedules.some(schedule => {
        const scheduleStart = new Date(schedule.start_ts);
        const scheduleEnd = new Date(schedule.end_ts);
        const newScheduleStart = new Date();
        const newScheduleEnd = new Date();
        newScheduleStart.setDate(scheduleStart.getDate() - 1);
        newScheduleEnd.setDate(scheduleEnd.getDate() - 1);
        return (dateWithoutTime <= scheduleStart && newScheduleStart < dateWithoutTime) || (dateWithoutTime <= scheduleEnd && newScheduleEnd < dateWithoutTime);
      });
      return hasEvent ? <div className="event-day-marker"></div> : null;
    }
    return null;
  };
  
  const handleAppointmentButtonClick = async (appointment) => 
  {

    try {
    var nome_paciente = null;
    if (appointment.paciente == null) {
      nome_paciente = "Sem paciente";
    }
    else {
      const res = await getUserById(appointment.paciente);
      nome_paciente = res.data.username;
    }
    console.log(nome_paciente)
    confirmAlert({
      title: 'Appointment Details',
      message: `Horario: ${new Date(appointment.start_ts).toLocaleString()} até ${new Date(appointment.end_ts).toLocaleString()}.\n`
        + `Paciente: ${nome_paciente}.\n`
        + `Localizacao: Rua Joaquim Joao 123.`
        ,
      buttons: [
        {
          label: 'Voltar',
          onClick: () => console.log('User clicked to return'),
        },
        {
          label: 'Cancelar agendamento',
          // todo: realmente fazer uma chamada para o backend para criar o agendamento
          onClick: () => deleteAppointment(appointment.id).then(response =>{
            console.log("Foi possível cancelar consulta: ", response.data);
          }).catch(error => {
            console.error("Error cancelling appointment:", error);
          })
        },
      ],
    });
    } catch (error) {
      console.error("Error getting name:", error);
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      await getUser();
      if (userData) {
        user_id = userData.user_id;
      }
      setLoading(false);
      console.log("user_id: ", user_id);
     fetchSchedules(user_id);  
    };
    fetchData();
  }, []);

  const fetchSchedules = (user_id) => {
        if(user_id){

            console.log(user_id);

            listAppointmentMedico(user_id)
            .then(response => {
                setSchedules(response.data);
                setLoading(false);
            })
            .catch(error => {
                console.error("Error fetching schedules:", error);
                setLoading(false);
            });
        }else{
            console.log("User not logged in.");
            setLoading(false);
        }
    };

    return (
      <div className = 'middle' style={{ margin: '2%' }}>
        <h2><strong>Seus Agendamentos:</strong></h2>
        {loading ? (
          <p>Carregando agendas...</p>
        ) : (
          <>
            {schedules.length > 0 ? (
              <>
                <ul>
                  {schedules
                    .slice() // Cria uma cópia do array para não modificar o original
                    .sort((a, b) => a.start_ts - b.start_ts) // Ordena as consultas por data crescente
                    .map((schedule, index) => (
                      <li key={schedule.id}>
                        <strong>Consulta {index + 1}:</strong> {new Date(schedule.start_ts).toLocaleString()} até{' '}
                        {new Date(schedule.end_ts).toLocaleString()}
                        <button
                        key={schedule.id}
                        onClick={() => handleAppointmentButtonClick(schedule)}
                        style = {{  margin: '1.5vh',}}
                        >Cancelar</button>
                        {/* Add additional schedule details as needed */}
                      </li>
                    ))}
                </ul>
                {/* Example: Display schedules in a calendar */}
                <div>
                  <Calendar value={closestEventDate} tileContent={tileContent} />
                  {/* Configure calendar settings based on your library's documentation */}
                  {/* Example: events={schedules.map(schedule => new Date(schedule.start_ts))} */}
                </div>
              </>
            ) : (
              <p style = {{fontSize : '20px'}}>Nenhum agendamento criado.</p>
            )}
          </>
        )}
      </div>
    
      );
    
};

export default ScheduleList;