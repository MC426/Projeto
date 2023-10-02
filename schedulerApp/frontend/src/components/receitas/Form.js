import React, { Component } from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import { addReceitas } from '../../actions/receitas';

export class Form extends Component {
  state = {
    nomeMedico: '',
    remedios: '',
    message: '',
  };

  static propTypes = {
    addReceitas: PropTypes.func.isRequired,
  };

  onChange = (e) => this.setState({ [e.target.nomeMedico]: e.target.value });

  onSubmit = (e) => {
    e.preventDefault();
    const { nomeMedico, remedios, message } = this.state;
    const receitas = { nomeMedico, remedios, message };
    this.props.addReceitas(receitas);
    this.setState({
      nomeMedico: '',
      remedios: '',
      message: '',
    });
  };

  render() {
    const { nomeMedico, remedios, message } = this.state;
    return (
      <div className="card card-body mt-4 mb-4">
        <h2>Adicionar Receitas</h2>
        <form onSubmit={this.onSubmit}>
          <div className="form-group">
            <label>Nome Medico</label>
            <input
              className="form-control"
              type="text"
              name="nomeMedico"
              onChange={this.onChange}
              value={nomeMedico}
            />
          </div>
          <div className="form-group">
            <label>Remedios</label>
            <input
              className="form-control"
              type="text"
              name="remedios"
              onChange={this.onChange}
              value={remedios}
            />
          </div>
          <div className="form-group">
            <label>Observacoes</label>
            <textarea
              className="form-control"
              type="text"
              name="message"
              onChange={this.onChange}
              value={message}
            />
          </div>
          <div className="form-group">
            <button type="submit" className="btn btn-primary">
              Enviar
            </button>
          </div>
        </form>
      </div>
    );
  }
}

export default connect(null, { addReceitas })(Form);