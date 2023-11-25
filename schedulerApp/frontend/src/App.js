import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './Pages/Home/Home/Home'
import Login from './Pages/Login/Login'
import Header from './Pages/Home/Header/Header'
import Footer from './Pages/Home/Fotter/Footer';
import Dashboard from './Pages/Profile/Dashboard/Dashboard'
import { useState, useEffect } from 'react';
import axios from 'axios';
import ScheduleForm from './Pages/Scheduler/ScheduleForm';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

const client = axios.create({
  baseURL: "http://localhost:8000"
});
function App() {
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchUserData = () => {

    const cookies = document.cookie.split('; ').reduce((cookieObject, cookie) => {
      const [name, value] = cookie.split('=');
      cookieObject[name] = value;
      return cookieObject;
    }, {});
    
    console.log("Running app to fetch user data: ", cookies, cookies.jwt);

    client.get("/api/user", 
    {
      withCredentials: true
    })
      .then(function (res) {
        if (res.data && res.data.email) {
          setUserData(res.data);
          console.log("logado", res.data);
        } else {
          setUserData(res.data);
        }
      })
      .catch(function (error) {
        setUserData(null);
      }).finally(() => {
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchUserData();
  }, []); // Only run once on component mount

  return (
    <Router>
      <Header loading={loading} userData={userData} />
      <Routes>
        <Route path="/" element = {<Home />} />
        <Route path="/home" element = {<Home  />} />
        <Route path="/login" element = {<Login userData={userData} setUserData={setUserData} />} />
        <Route path="/profile" element = {<Dashboard  userData={userData} setUserData={setUserData} />} />
        <Route path="/agenda" element = {<ScheduleForm userData={userData}  />} />
      </Routes>
      <Footer/>
    </Router>
  );
}

export default App;