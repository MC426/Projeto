import React from 'react';
import './Banner.css';
import Lottie from 'lottie-react';
import animationData from './Animations/medical-animation.json';

const Banner = () => {
  return (
    <div className = "banner">
        <div class="text-container">
            <h1 style = {{fontSize : '10vh'}}><strong>Agenda+</strong></h1>
            <h2>Agende suas consultas na palma da mão</h2>
            <h5>Para médicos, gerencie seus horários, salas e pacientes.</h5>
            <h5>Para pacientes, escolha horários e médicos disponíveis. </h5>
        </div>
        <div className="lottie-container">
          <Lottie animationData={animationData}/>
        </div>
    </div>
  );
}

export default Banner;
