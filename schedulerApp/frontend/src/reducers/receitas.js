import { GET_RECEITAS, ADD_RECEITAS, DELETE_RECEITAS, CLEAR_RECEITAS } from '../actions/types.js';

const initialState = {
  receitas: [],
};

export default function (state = initialState, action) {
  switch (action.type) {
    case GET_RECEITAS:
      return {
        ...state,
        receitas: action.payload,
      };
    case DELETE_RECEITAS:
      return {
        ...state,
        receitas: state.receitas.filter((receita) => receita.id !== action.payload),
      };
    case ADD_RECEITAS:
      return {
        ...state,
        receitas: [...state.receitas, action.payload],
      };
    case CLEAR_RECEITAS:
      return {
        ...state,
        receitas: [],
      };
    default:
      return state;
  }
}