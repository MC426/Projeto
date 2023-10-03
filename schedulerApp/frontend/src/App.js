import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './Pages/Home/Home/Home'
import Login from './Pages/Login/Login'
import Header from './Pages/Home/Header/Header.jsx'
import Footer from './Pages/Home/Fotter/Footer';
import Dashboard from './Pages/Profile/Dashboard/Dashboard'

function App() {
  return (
    <Router>
      <Header/>
      <Routes>
        <Route path="/" element = {<Home />} />
        <Route path="/home" element = {<Home />} />
        <Route path="/login" element = {<Login />} />
        <Route path="/profile" element = {<Dashboard />} />
      </Routes>
      <Footer/>
    </Router>

  );
}

export default App;