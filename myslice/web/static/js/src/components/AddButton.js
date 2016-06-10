var React = require('react');

module.exports = React.createClass({
    render: function() {
        return (
            <button className="elementAdd" onClick={this.props.handleClick}><img className="icon" src="/static/icons/plus.png" alt="+" /> {this.props.label}</button>
        );
    }
});