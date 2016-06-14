import React from 'react';

class Button extends React.Component {

    render() {
        return (
            <button className="{this.props.class}" onClick={this.props.handleClick} >
                <img className="icon" src="/static/icons/{this.props.icon}.png" alt="{this.props.label}" />
                {this.props.label}
            </button>
        );
    }
}

export default Button;