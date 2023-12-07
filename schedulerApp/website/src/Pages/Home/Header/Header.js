import React from 'react';
import { Container, Nav, Navbar } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import logo from '../../../Images/logo ic.png';
import './Header.css';
import { useEffect } from 'react';
import { useUser } from './../../../UserProvider';

const Header = ({loading}) => {
  const { userData, getUser } = useUser();
  useEffect(() => {
    console.log("header tenta dar get user");
  }, [userData, loading]);

  return (
        <div className="head-bg">
            <Navbar className="navbar" collapseOnSelect expand="lg">
                <Container className="container-head">
                    <Navbar.Brand href="/home"><img src={logo} alt="logo" /></Navbar.Brand>
                    <Navbar.Toggle aria-controls="basic-navbar-nav" expand="lg"/>
                    <Navbar.Collapse id="basic-navbar-nav">
                        <Nav className="ms-auto align-items-center">
                            <Link to="/home" className='list-item text-decoration-none'>Home</Link>
                            <Link to="/about" className='list-item text-decoration-none'>Sobre</Link>
                            <Link to="/escolher-horario" className='list-item text-decoration-none'>Escolher um horario</Link>
                            <Link to="/listar-agenda" className='list-item text-decoration-none'>Mostrar agenda</Link>
                            <Link to="/agenda" className='list-item text-decoration-none'>Criar agenda</Link>
                            {
                            userData
                            ?
                            <Link to="/profile" type="button" className="btn btn-danger">Profile</Link>
                            :
                            <Link to="/login" type="button" className="btn btn-danger">Login</Link>
                            }
                        </Nav>
                    </Navbar.Collapse>
                </Container>
            </Navbar>
        </div>
    );
};

export default Header;