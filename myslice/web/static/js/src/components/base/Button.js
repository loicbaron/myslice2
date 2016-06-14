import React from 'react';

class Button extends React.Component {

    render() {

        var icon = "fa fa-" + this.props.icon + " fa-lg";

        if (this.props.active) {
            var className = 'active';
        } else {
            var className = '';
        }

        return (
            <button className={className} onClick={this.props.handleClick} >
                <i className={icon}></i>&nbsp;&nbsp;
                {this.props.label}
            </button>
        );

    }
}

export default Button;