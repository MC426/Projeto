import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './Pages/Home/Home/Home'
import Login from './Pages/Login/Login'
import Header from './Pages/Home/Header/Header.jsx'
import Footer from './Pages/Home/Fotter/Footer';
import React, {Component, Fragment} from 'react';
import {Provider} from 'react-redux'
import store from './store';

class App extends Component {
  // componentDidMount() {
  //   store.dispatch(loadUser());
  // }
  render(){
    return (
      <Provider store={store}>
        <Router>
          <Header/>
          <Routes>
            <Route path="/" element = {<Home />} />
            <Route path="/home" element = {<Home />} />
            <Route path="/login" element = {<Login />} />
          </Routes>
          <Footer/>
        </Router>
      </Provider>
    );
  }
}

export default App;