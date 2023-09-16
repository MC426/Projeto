import React, { useState } from 'react';
import axios from "axios";

function CreateAppointment() {
  const [formData, setFormData] = useState({
    start_time: '',
    end_time: '',
    max_capacity: 0,
    current_capacity: 0,
    location: '',
    hospital_or_clinic_name: '',
    medic_name: '',
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN';
    // axios.defaults.xsrfCookieName = 'csrftoken';

    axios
      .post('/api/appointments/', formData, {
        headers: {
          'Content-Type': 'application/json',
        },
      })
      .then((response) => {
        // Handle success or display a success message
        console.log('Appointment created:', response.data);

        // Reset the form data
        setFormData({
          start_time: '',
          end_time: '',
          max_capacity: 0,
          current_capacity: 0,
          location: '',
          hospital_or_clinic_name: '',
          medic_name: '',
        });
      })
      .catch((error) => console.error('Error creating appointment:', error));
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  return (
    <div>
      <h2>Create Appointment</h2>
      <form onSubmit={handleSubmit}>
        {/* Add form fields for each appointment property */}
        <div>
        <label htmlFor="start_time">Start Time:</label>
          <input
            type="datetime-local"
            id="start_time"
            name="start_time"
            value={formData.start_time}
            onChange={handleChange}
          />
        </div>
        <div>
          <label htmlFor="end_time">End Time:</label>
          <input
            type="datetime-local"
            id="end_time"
            name="end_time"
            value={formData.end_time}
            onChange={handleChange}
          />
        </div>
        <div>
          <label htmlFor="max_capacity">Max Capacity:</label>
          <input
            type="number"
            id="max_capacity"
            name="max_capacity"
            value={formData.max_capacity}
            onChange={handleChange}
          />
        </div>
        <div>
          <label htmlFor="location">Location:</label>
          <input
            type="text"
            id="location"
            name="location"
            value={formData.location}
            onChange={handleChange}
          />
        </div>
        <div>
          <label htmlFor="medic_name">Medic Name:</label>
          <input
            type="text"
            id="medic_name"
            name="medic_name"
            value={formData.medic_name}
            onChange={handleChange}
          />
        </div>
        {/* Add other form fields here */}
        <button type="submit">Create Appointment</button>
      </form>
    </div>
  );
}

export default CreateAppointment;
