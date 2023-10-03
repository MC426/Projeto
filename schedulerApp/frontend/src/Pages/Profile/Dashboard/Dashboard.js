import React from 'react';
import { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';


axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

const client = axios.create({
  baseURL: "http://127.0.0.1:8000"
});


const Dashboard = () => {
    const [userData, setUserData] = useState(null);

    useEffect(() => {
        const fetchUserData = async () => {
          try {
            const response = await fetch('/api/user');
            const data = await response.json();
            setUserData(data);
          } catch (error) {
            console.error('Error fetching user data:', error);
          }
        };
      
        fetchUserData();
      }, []);
    
  function submitLogout(e) {
        e.preventDefault();
        client.post(
        "/api/logout",
        {withCredentials: true}
        ).then(function(res) {
            setUserData(null);
        });
    }

  return (
    <div>
          {userData ?
    (<>
    <div className="container mt-5">
      <div className="row">
        {/* Profile Information */}
        <div className="col-md-4">
          <div className="card">
            <img
              src="profile-image.jpg"
              className="card-img-top"
              alt="Profile Image"
            />
            <div className="card-body">
              <h5 className="card-title"> {userData.name} </h5>
              <p className="card-text"> {userData.email} </p>
            </div>
          </div>
        </div>

        {/* Dashboard Content */}
        <div className="col-md-8">
          <div className="card">
            <div className="card-body">
              <h5 className="card-title">Página de perfil</h5>
              <p className="card-text">
                Bem vindo a sua página de perfil. Aqui você pode ver suas consultas, suas receitas e seus dados.
              </p>
            </div>
          </div>

          {/* Sample Action Buttons */}
          <div className="mt-3">
            <button className="btn btn-primary">Editar Perfil</button>
            <Link to="/home" type="button" className="btn btn-danger" onClick={submitLogout}>Logout</Link>
          </div>
        </div>
      </div>
    </div></>)
    : (<div> Please login first </div>)}
    </div>
  );
};

export default Dashboard;
