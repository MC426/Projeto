import React, { useState, useEffect } from 'react';
import Datetime from 'react-datetime';
import 'react-datetime/css/react-datetime.css';
import { useUser } from './../../UserProvider';
import axios from 'axios';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

const client = axios.create({
  baseURL: "http://localhost:8000"
});

const ScheduleForm = () => {
  const { userData, getUser } = useUser();
  const [successMessage, setSuccessMessage] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);
  const [formData, setFormData] = useState({
    start_time: '',
    end_time: '',
  });

  var user_id = null;
  const getUserId = () => {
    getUser();
    if(userData)
      user_id = userData.user_id;
    return user_id;
  };


  const handleChange = (name, value) => {
    setFormData({
      ...formData,
      [name]: value,
    });
  };
  const dateToString = (date) => {
    return date.toISOString().slice(0, 19).replace('T', ' ');
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle form submission logic here
    getUserId();
    console.log('Form data submitted:', formData);
    const requestData = {
      start_ts: dateToString(formData.start_time),
      end_ts: dateToString(formData.end_time),
      medico: user_id
    };
    console.log(requestData);

    client.post(
      "/api/scheduler/create-appointment",
      requestData,
      {withCredentials: true},
    ).then(function(res) {
      console.log(res.data);
      setSuccessMessage("Horario criado com sucesso!");
      setErrorMessage(null);
    }).catch(function(error){
      console.log("Error on submitting schedule.");
      console.log(error);
      setErrorMessage("Erro ao criar horario, tente novamente.");
      setSuccessMessage(null);
    });
  
  };

  return (
    <div style = {{margin: '2%'}}>
      <h2><strong>Crie um horario de Agendamento</strong></h2>
      {successMessage && <div style={{ color: 'green' }}>{successMessage}</div>}
      {errorMessage && <div style={{ color: 'red' }}>{errorMessage}</div>}
      
      <form onSubmit={handleSubmit}>
        <div style={{marginTop: '1vh', marginBottom: '1vh'}} >
          <label >Inicio:</label>
          <Datetime
            dateFormat="YYYY-MM-DD"
            timeFormat="HH:mm:ss"
            onChange={(value) => handleChange('start_time', value)}
            value={formData.start_time}
          />
        </div>
        <div style={{marginTop: '1vh', marginBottom: '1vh'}} >
          <label>Fim:</label>
          <Datetime
            dateFormat="YYYY-MM-DD"
            timeFormat="HH:mm:ss"
            onChange={(value) => handleChange('end_time', value)}
            value={formData.end_time}
          />
        </div>
        <div>
          <button type="submit">Enviar</button>
        </div>
      </form>
    </div>
  );
};

export default ScheduleForm;
