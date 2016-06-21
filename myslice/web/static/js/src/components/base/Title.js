import React from 'react';

class Title extends React.Component {
  render() {

      return <h1>{this.props.title} <span>{this.props.subtitle}</span></h1>;
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