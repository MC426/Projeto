import React from 'react';
import { Link } from 'react-router-dom';
import Banner from '../Banner/Banner';
import HomeInfo from '../HomeInfo/HomeInfo'
import Dashboard from '../../../components/receitas/Dashbord';

const Home = () => {
  return (
    <>
       <Banner />
       <HomeInfo />
    </>
  );

}

export default Home;
