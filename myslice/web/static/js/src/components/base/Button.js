import React from 'react';

const Button = (props) => {
        var className;
        var icon = "fa fa-" + props.icon + " fa-lg";

        props.active ? className = 'active' : className = '';

        return (
            <button className={className} onClick={props.handleClick} >
                <i className={icon}></i>&nbsp;&nbsp;
                {props.label}
            </button>
        );

};

Button.propTypes = {
    icon: React.PropTypes.string,
    label: React.PropTypes.string,
    active: React.PropTypes.bool,
    handleClick: React.PropTypes.func
};

Button.defaultProps = {
    icon: 'question',
    label: null,
    active: false
};

export default Button;