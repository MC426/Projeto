import logo from './logo.svg';
import React from 'react';
import './App.css';
import { Container } from 'react-bootstrap';
import ListAppointments from './Appointment/ListAppointments'; // Import the ListAppointments component
import CreateAppointment from './Appointment/CreateAppointment'; // Import the CreateAppointment component

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Medical Appointment Scheduler</h1>
      </header>
      <Container>
        <ListAppointments /> {
          /* Render the ListAppointments component */
        }
        <CreateAppointment /> {
          /* Render the CreateAppointment component */
        }
      </Container>
    </div>
  );
}

export default App;
