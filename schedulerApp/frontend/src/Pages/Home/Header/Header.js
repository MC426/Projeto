import React from 'react';
import { Container, Nav, Navbar } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import logo from '../../../Images/logo ic.png';
import './Header.css';
import { useEffect } from 'react';

const Header = ({loading, userData}) => {
  useEffect(() => {
    console.log('userData has changed at header:', userData, loading);
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
                            <Link to="/service" className='list-item text-decoration-none'>Serviços</Link>
                            <Link to="/hospital" className='list-item text-decoration-none'>Hospitais</Link>
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