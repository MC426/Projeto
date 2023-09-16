import React, { useState } from 'react';

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

    // Send a POST request to your backend API to create a new appointment
    // Replace this with your actual API endpoint and request configuration
    fetch('/api/appointments/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),
    })
      .then((response) => response.json())
      .then((data) => {
        // Handle success or display a success message
        console.log('Appointment created:', data);

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
          <label htmlFor="hospital_or_clinic_name">Hospital/Clinic Name:</label>
          <input
            type="text"
            id="hospital_or_clinic_name"
            name="hospital_or_clinic_name"
            value={formData.hospital_or_clinic_name}
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
