import { faUser } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import React from 'react';
import { Container, Nav, Navbar } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import logo from '../../../Images/logo ic.png';
import './Header.css';
import { useState, useEffect } from 'react';
import axios from 'axios';


axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;



const Header = () => {

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
                            <Link to="/contact" className='list-item text-decoration-none'>Contato</Link>
                            {
                            // userData 
                            // ?
                            <Link to="/profile" type="button" className="btn btn-danger">Profile</Link>
                            // <button type="button" className="btn btn-danger" onClick={submitLogout}>Log Out</button>
                            // :
                            // <Link to="/login" type="button" className="btn btn-danger">Login</Link>
                            }
                            {/* {userData &&
                                <Navbar.Text><FontAwesomeIcon icon={faUser} /><span className="userName">{userData.email}</span></Navbar.Text>
                            } */}
                        </Nav>
                    </Navbar.Collapse>
                </Container>
            </Navbar>
        </div>
    );
};

export default Header;