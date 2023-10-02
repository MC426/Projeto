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
      </Fragment>
    );
  }
}

const mapStateToProps = (state) => ({
  receitas: state.receitas.receitas,
});

export default connect(mapStateToProps, { getReceitas, deleteReceitas })(Receitas);