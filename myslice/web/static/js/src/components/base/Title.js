import React from 'react';

const Title = ({title, subtitle, separator}) => {
    let sub = null;
    let sep = null;

    if (subtitle) {
        sub = <span className="subtitle">{subtitle}</span>;
    }

    if (separator) {
        sep = <span className="separator">{separator}</span>;
    }
    return <h2>{title}{sep}{sub}</h2>;

};

Title.propTypes = {
    title: React.PropTypes.string.isRequired,
    subtitle: React.PropTypes.string

};

Title.defaultProps = {
    subtitle: ''
};

export default Title;