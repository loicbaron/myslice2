var React = require('react');

module.exports = React.createClass({

    getInitialState () {
        return {
            'class' : '',
        }
    },

    validateEmail(email) {
    	var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    	return re.test(email);
	},

    updateEmail(event) {
        var email = event.target.value;

        if (this.validateEmail(email)) {
            this.setState({'class' : ''});
            this.props.handleChange(email);
        } else {
            this.setState({'class' : 'error'});
        }
    },

    render: function () {
        return (
            <input onChange={this.updateEmail} className={this.state.class} placeholder="Email address" type="text" name="email" />
        );
    }
});