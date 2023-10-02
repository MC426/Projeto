import React, { Fragment } from 'react';
import Form from './Form';
import Receitas from './Receitas';

const Dashboard = () => {
  return (
    <Fragment>
      <Form />
      <Receitas />
    </Fragment>
  );
}

export default Dashboard;