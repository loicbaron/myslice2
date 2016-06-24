import React from 'react';

class SectionTitle extends React.Component {
  render() {

      return <h3>{this.props.title} <span>{this.props.subtitle}</span></h3>;
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