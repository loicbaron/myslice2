import React from 'react';

class SectionTitle extends React.Component {
  render() {

      return <h2>{this.props.title} <span>{this.props.subtitle}</span></h2>;
  }
}

SectionTitle.propTypes = {
    title: React.PropTypes.string.isRequired,
    subtitle: React.PropTypes.string
};

SectionTitle.defaultProps = {
    subtitle: ''
};

export default SectionTitle;