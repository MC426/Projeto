import React from 'react';
import { Col, Container, NavLink, Row } from 'react-bootstrap';
import './Footer.css'

const Footer = () => {
    return (
        <div className="footer-bg">
            <div className="footer-copy-right text-center text-white">
                <p className='mb-0'>&copy; 2023 - <span className="developer">Projeto de MC426 - UNICAMP - IC</span> </p>
            </div>
        </div>
    );
};

export default Footer;