import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './Pages/Home/Home/Home'
import Login from './Pages/Login/Login'
import Header from './Pages/Home/Header/Header'
import Footer from './Pages/Home/Fotter/Footer';
import Dashboard from './Pages/Profile/Dashboard/Dashboard'
import ScheduleForm from './Pages/Scheduler/ScheduleForm';
import ScheduleList from './Pages/ListSchedule/ListSchedule';
import ListAvailableTimes from './Pages/ListAvailableTimes/ListAvailableTimes';

function App() {

  return (
      <Router>
        <Header />
        <Routes>
          <Route path="/" element = {<Home />} />
          <Route path="/home" element = {<Home  />} />
          <Route path="/login" element = {<Login />} />
          <Route path="/profile" element = {<Dashboard  />} />
          <Route path="/agenda" element = {<ScheduleForm />} />
          <Route path="/listar-agenda" element = {<ScheduleList />} />
          <Route path="escolher-horario" element = {<ListAvailableTimes />} />
        </Routes>
        <Footer/>
      </Router>
  );
}

export default App;