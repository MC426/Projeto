import { faUser } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import React from 'react';
import { Container, Nav, Navbar } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import logo from '../../../Images/logo ic.png';
import './Header.css';

const Header = () => {

    // const [currentUser, setCurrentUser] = useState();
    // const [email, setEmail] = useState('');

    // useEffect(() => {
    //     client.get("/api/user")
    //     .then(function(res) {
    //     setCurrentUser(true);
    //     })
    //     .catch(function(error) {
    //     setCurrentUser(false);
    //     });
    // }, []);
    const client = "cliente";
    const user = "usuario";

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
                            {/* {user.email 
                            ?
                            <button type="button" className="btn btn-danger" onClick={logout}>Log Out</button>
                            :
                            <Link to="/login" type="button" className="btn btn-danger">Login</Link>
                            }
                            {user.email &&
                                <Navbar.Text><FontAwesomeIcon icon={faUser} /><span className="userName">{user.displayName}</span></Navbar.Text>
                            } */}
                        </Nav>
                    </Navbar.Collapse>
                </Container>
            </Navbar>
        </div>
    );
};

export default Header;