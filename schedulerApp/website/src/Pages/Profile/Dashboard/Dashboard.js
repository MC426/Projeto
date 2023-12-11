import React from 'react';
import { Link } from 'react-router-dom';
import { useEffect } from 'react';
import { useUser } from '../../../backendFacade';


const Dashboard = () => {
  const { userData, getUser, logoutUser } = useUser();

  useEffect(() => {
    getUser();
  }, []); 
  
  function submitLogout(e) {
    e.preventDefault();
    console.log("dashboard tenta dar logout");
    logoutUser();
    console.log(userData);
  }

  return (
    <div >
          {userData ?
    (<>
    <div className="container mt-5">
      <div className="row">
        {/* Profile Information */}
        <div className="col-md-4">
          <div className="card">
            <div className="card-body">
              <h5 className="card-title"> Usuário: {userData.username} </h5>
              <p className="card-text"> Email: {userData.email} </p>
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
          <div className="mt-3" style = {{margin : '2vh'}}>
            <button className="btn btn-primary">Editar Perfil</button>
            <Link to="/home" type="button" className="btn btn-danger" onClick={submitLogout}>Logout</Link>
          </div>
        </div>
      </div>
    </div></>)
    : (<div style = {{textAlign : 'center'}}> <h1>Por favor faça login primeiro</h1> 
    </div>)}
    </div>
  );
};

export default Dashboard;
