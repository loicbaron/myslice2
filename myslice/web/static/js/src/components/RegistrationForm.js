var React = require('react');
var store = require('../stores/RegistrationStore');
var AuthoritiesSelect = require('./AuthoritiesSelect');

module.exports = React.createClass({

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

    render: function () {
        return (
            <form method="post">
                <div className="registration-authority">
                    <AuthoritiesSelect />
                </div>
                <div className="registration-email">
                    <input class="form-control" placeholder="Email address" type="text" name="email" />
                </div>
                <div className="registration-firstname">
                    <input class="form-control" placeholder="First name" type="text" name="firstname" />
                </div>
                <div className="registration-lastname">
                    <input class="form-control" placeholder="Last name" type="text" name="lastname" />
                </div>
                <div className="registration-submit">
                    <button type="submit" className="btn btn-default">Submit</button>
                </div>
            </form>
        );

    }

});
