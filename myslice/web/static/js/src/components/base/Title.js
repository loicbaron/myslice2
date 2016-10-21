import React from 'react';

const Title = ({title, subtitle}) =>
    <h2>{title} <span>{subtitle}</span></h2>;

Title.propTypes = {
    title: React.PropTypes.string.isRequired,
    subtitle: React.PropTypes.string

};

Title.defaultProps = {
    subtitle: ''
};

export default Title;