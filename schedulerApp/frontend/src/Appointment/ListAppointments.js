import React, { useEffect, useState } from 'react';
import axios from 'axios';

function ListAppointments() {
    const [appointments, setAppointments] = useState([]);
  
    useEffect(() => {

      axios
        .get('/api/appointments/')
        .then((response) => {
          const data = response.data;
            setAppointments(data);
        })
        .catch((error) => console.error('Error fetching appointments:', error));
    }, []);
  
    console.log("trying to do something");
    return (
      <div>
        <h2>Appointments</h2>
        <ul>
          {appointments.map((appointment) => (
            <li key={appointment.id}>
              {appointment.hospital_or_clinic_name} - {appointment.medic_name} - {appointment.start_time}
            </li>
          ))}
        </ul>
      </div>
    );
  }
  

export default ListAppointments;
