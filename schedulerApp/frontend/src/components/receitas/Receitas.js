import React, { Component, Fragment } from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import { getReceitas, deleteReceitas } from '../../actions/receitas';

export class Receitas extends Component {
  static propTypes = {
    receitas: PropTypes.array.isRequired,
    getReceitas: PropTypes.func.isRequired,
    deleteReceitas: PropTypes.func.isRequired,
  };

  componentDidMount() {
    this.props.getReceitas();
  }

  render() {
    return (
      <Fragment>
        <h2>Receitas</h2>
        {/* <table className="table table-striped">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Email</th>
              <th>Message</th>
              <th />
            </tr>
          </thead>
          <tbody>
            {this.props.leads.map((lead) => (
              <tr key={lead.id}>
                <td>{lead.id}</td>
                <td>{lead.name}</td>
                <td>{lead.email}</td>
                <td>{lead.message}</td>
                <td>
                  <button
                    onClick={this.props.deleteLead.bind(this, lead.id)}
                    className="btn btn-danger btn-sm"
                  >
                    {' '}
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table> */}
      </Fragment>
    );
  }
}

const mapStateToProps = (state) => ({
  receitas: state.receitas.receitas,
});

export default connect(mapStateToProps, { getReceitas, deleteReceitas })(Receitas);