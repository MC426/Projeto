import axios from 'axios';
import { createMessage, returnErrors } from './messages';
import { tokenConfig } from './auth';

import { GET_RECEITAS, ADD_RECEITAS, DELETE_RECEITAS } from './types';

// GET RECEITAS
export const getReceitas = () => (dispatch, getState) => {
  axios
    .get('/api/receitas/', tokenConfig(getState))
    .then((res) => {
      dispatch({
        type: GET_RECEITAS,
        payload: res.data,
      });
    })
    .catch((err) => dispatch(returnErrors(err.response.data, err.response.status)));
};

// DELETE RECEITAS
export const deleteReceitas = (id) => (dispatch, getState) => {
  axios
    .delete(`/api/receitas/${id}/`, tokenConfig(getState))
    .then((res) => {
      dispatch(createMessage({ deleteReceitas: 'Lead Deleted' }));
      dispatch({
        type: DELETE_RECEITAS,
        payload: id,
      });
    })
    .catch((err) => console.log(err));
};

// ADD LEAD
export const addLead = (lead) => (dispatch, getState) => {
  axios
    .post('/api/leads/', lead, tokenConfig(getState))
    .then((res) => {
      dispatch(createMessage({ addLead: 'Lead Added' }));
      dispatch({
        type: ADD_LEAD,
        payload: res.data,
      });
    })
    .catch((err) => dispatch(returnErrors(err.response.data, err.response.status)));
};