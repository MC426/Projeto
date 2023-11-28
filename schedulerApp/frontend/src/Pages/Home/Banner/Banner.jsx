import React from 'react';
import './Banner.css';
import Lottie from 'lottie-react';
import animationData from './Animations/medical-animation.json';

const Banner = () => {
  return (
    <div className = "banner">
        <div class="text-container">
            <h1>Projeto MC426</h1>
            <h2>Esse é um projeto feito por alunos da UNICAMP para a matéria de engenharia de Software.</h2>
        </div>
        <div className="lottie-container">
          <Lottie animationData={animationData}/>
        </div>
    </div>
  );
}

export default Banner;
