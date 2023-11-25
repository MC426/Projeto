import React from 'react';
import { useState, useEffect } from 'react';
import axios from 'axios';
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';


axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

const client = axios.create({
  baseURL: "http://localhost:8000"
});

const Login = ({userData, setUserData}) => {
    const [registrationToggle, setRegistrationToggle] = useState(false);
    const [email, setEmail] = useState('');
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    useEffect(() => {
      const cookies = document.cookie.split('; ').reduce((cookieObject, cookie) => {
        const [name, value] = cookie.split('=');
        cookieObject[name] = value;
        return cookieObject;
      }, {});
      

      console.log("Login: ", cookies, cookies.jwt);

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
        });
    }, []);
    

    function update_form_btn() {
        if (registrationToggle) {
        document.getElementById("form_btn").innerHTML = "Register";
        setRegistrationToggle(false);
        } else {
        document.getElementById("form_btn").innerHTML = "Log in";
        setRegistrationToggle(true);
        }
    }

    function submitRegistration(e) {
        e.preventDefault();
        client.post(
        "/api/register",
        {
            email: email,
            username: username,
            password: password
        }
        ).then(function(res) {
        client.post(
            "/api/login",
            {
            email: email,
            password: password
            }
        ).then(function(res) {
          console.log(res.data);
          setUserData(res.data);
          const token = res.data.jwt
          document.cookie = `jwt=${token}; path=/`;
        }).catch(function(error){
          console.log("Error");
        });
        });
    }

    function submitLogin(e) {
        e.preventDefault();
        client.post(
        "/api/login",
        {
            email: email,
            password: password
        }
        ).then(function(res) {
          console.log(res.data);
          setUserData(res.data);
          const token = res.data.jwt
          document.cookie = `jwt=${token}; path=/`;
        }).catch(function(error){
          console.log("Error on login.");
          console.log(error);
        });
    }

    function submitLogout(e) {
        e.preventDefault();
        client.post(
        "/api/logout",
        {withCredentials: true}
        ).then(function(res) {
          setUserData(null);
        });
    }

  if (userData) {
    return (
      <div>
        <Navbar bg="dark" variant="dark">
          <Container>
            <Navbar.Brand>Voce esta loggado</Navbar.Brand>
            <Navbar.Toggle />
            <Navbar.Collapse className="justify-content-end">
              <Navbar.Text>
                <form onSubmit={e => submitLogout(e)}>
                  <Button type="submit" variant="light">Log out</Button>
                </form>
              </Navbar.Text>
            </Navbar.Collapse>
          </Container>
        </Navbar>
          <div className="center">
            <h2>You're logged in!</h2>
          </div>
          
        </div>
    );
  }
  return (
    <div>
    <Navbar bg="dark" variant="dark">
      <Container>
        <Navbar.Brand>Faça seu login</Navbar.Brand>
        <form onSubmit={e => submitLogout(e)}>
                  <Button type="submit" variant="light">Log out</Button>
                </form>
        <Navbar.Toggle />
        <Navbar.Collapse className="justify-content-end">
          <Navbar.Text>
            <Button id="form_btn" onClick={update_form_btn} variant="light">Register</Button>
          </Navbar.Text>
        </Navbar.Collapse>
      </Container>
    </Navbar>
    {
      registrationToggle ? (
        <div className="center">
          <Form onSubmit={e => submitRegistration(e)}>
            <Form.Group className="mb-3" controlId="formBasicEmail">
              <Form.Label>Email address</Form.Label>
              <Form.Control type="email" placeholder="Enter email" value={email} onChange={e => setEmail(e.target.value)} />
              <Form.Text className="text-muted">
                We'll never share your email with anyone else.
              </Form.Text>
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicUsername">
              <Form.Label>Username</Form.Label>
              <Form.Control type="text" placeholder="Enter username" value={username} onChange={e => setUsername(e.target.value)} />
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicPassword">
              <Form.Label>Password</Form.Label>
              <Form.Control type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
            </Form.Group>
            <Button variant="primary" type="submit">
              Submit
            </Button>
          </Form>
        </div>        
      ) : (
        <div className="center">
          <Form onSubmit={e => submitLogin(e)}>
            <Form.Group className="mb-3" controlId="formBasicEmail">
              <Form.Label>Email address</Form.Label>
              <Form.Control type="email" placeholder="Enter email" value={email} onChange={e => setEmail(e.target.value)} />
              <Form.Text className="text-muted">
                We'll never share your email with anyone else.
              </Form.Text>
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicPassword">
              <Form.Label>Password</Form.Label>
              <Form.Control type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
            </Form.Group>
            <Button variant="primary" type="submit">
              Submit
            </Button>
          </Form>
        </div>
      )
    }
    </div>
  );
}

export default Login;