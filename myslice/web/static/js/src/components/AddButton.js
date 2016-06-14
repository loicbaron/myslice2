import React from 'react';

export default class AuthoritiesSelect extends React.Component {

    render() {
        return (
            <button className="elementAdd" onClick={this.props.handleClick} >
                <img className="icon" src="/static/icons/plus.png" alt="+" /> 
                {this.props.label}
            </button>
        );
    }
}