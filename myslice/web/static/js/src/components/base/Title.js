import React from 'react';

class Title extends React.Component {
  render() {

      return <h2>{this.props.title} <span>{this.props.subtitle}</span></h2>;
  }
}

Title.propTypes = {
    title: React.PropTypes.string.isRequired,
    subtitle: React.PropTypes.string
};

Title.defaultProps = {
    subtitle: ''
};

export default Title;