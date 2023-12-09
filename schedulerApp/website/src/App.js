import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './Pages/Home/Home/Home';
import Login from './Pages/Login/Login';
import Header from './Pages/Home/Header/Header';
import Footer from './Pages/Home/Footer/Footer';
import Dashboard from './Pages/Profile/Dashboard/Dashboard';
import ScheduleForm from './Pages/Scheduler/ScheduleForm';
import ScheduleList from './Pages/ListSchedule/ListSchedule';
import ListAvailableTimes from './Pages/ListAvailableTimes/ListAvailableTimes';
import PrivateRoute from './PrivateRoute'; // Importe o componente PrivateRoute aqui

function App() {
  return (
    <Router>
      <Header />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route 
          path="/profile" 
          element={
            <PrivateRoute>
              <Dashboard />
            </PrivateRoute>
          } 
        />
        <Route 
          path="/agenda" 
          element={
            <PrivateRoute>
              <ScheduleForm />
            </PrivateRoute>
          } 
        />
        <Route 
          path="/listar-agenda" 
          element={
            <PrivateRoute>
              <ScheduleList />
            </PrivateRoute>
          } 
        />
        <Route 
          path="/escolher-horario" 
          element={
            <PrivateRoute>
              <ListAvailableTimes />
            </PrivateRoute>
          } 
        />
      </Routes>
      <Footer />
    </Router>
  );
}

export default App;
