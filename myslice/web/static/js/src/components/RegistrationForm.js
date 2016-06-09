var React = require('react');
var actions = require('../actions/RegistrationActions');
var store = require('../stores/RegistrationStore');
var AuthoritiesSelect = require('./AuthoritiesSelect');
var EmailInput = require('./EmailInput');
var LoadingPanel = require('./LoadingPanel');

module.exports = React.createClass({

    propTypes: {
        handleChange: React.PropTypes.func
    },

    getInitialState () {
        return store.getState();
    },

    componentDidMount: function() {
        store.listen(this.onChange);
    },

    componentWillUnmount() {
        store.unlisten(this.onChange);
    },

    onChange(state) {
        this.setState(state);
    },

    updateAuthority(value) {
        actions.updateAuthority(value);
    },

    updateEmail(value) {
        actions.updateEmail(value);
    },

    updateFirstname(event) {
        actions.updateFirstname(event.target.value);
    },

    updateLastname(event) {
        actions.updateLastname(event.target.value);
    },

    submitForm(event) {
        event.preventDefault();
        actions.submitForm();
    },

    render: function () {
        return (
            <form onSubmit={this.submitForm}>
                <div className="registration-authority">
                    <AuthoritiesSelect handleChange={this.updateAuthority} />
                </div>
                <div className="registration-email">
                    <EmailInput handleChange={this.updateEmail} />
                </div>
                <div className="registration-firstname">
                    <input onChange={this.updateFirstname} placeholder="First name" type="text" name="firstname" />
                </div>
                <div className="registration-lastname">
                    <input onChange={this.updateLastname} placeholder="Last name" type="text" name="lastname" />
                </div>
                <div className="registration-submit">
                    <input type="submit" className="btn btn-default" />
                </div>
                <LoadingPanel show={this.state.loading} />
            </form>
        );

    }

});
