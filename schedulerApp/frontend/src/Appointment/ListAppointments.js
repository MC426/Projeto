import React, { useEffect, useState } from 'react';

function ListAppointments() {
  const [appointments, setAppointments] = useState([]);

  useEffect(() => {
    // Fetch appointments from your backend API here
    // Replace this with your actual API endpoint
    fetch('/api/appointments/')
      .then((response) => response.json())
      .then((data) => {
        // Set the fetched appointments directly
        setAppointments(data);
      })
      .catch((error) => console.error('Error fetching appointments:', error));
  }, []);

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
