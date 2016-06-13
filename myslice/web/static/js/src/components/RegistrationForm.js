import React from 'react';
import actions from '../actions/RegistrationActions';
import store from '../stores/RegistrationStore';
import AuthoritiesSelect from './AuthoritiesSelect';
import EmailInput from './EmailInput';
import LoadingPanel from './LoadingPanel';

class RegistrationForm extends React.Component {

    constructor(props) {
        super(props);
        this.state = store.getState();
        this.onChange = this.onChange.bind(this);
    }

    componentDidMount() {
        store.listen(this.onChange);
    }

    componentWillUnmount() {
        store.unlisten(this.onChange);
    }

    onChange(state) {
        this.setState(state);
    }

    updateAuthority(value) {
        actions.updateAuthority(value);
    }

    updateEmail(value) {
        actions.updateEmail(value);
    }

    updateFirstname(event) {
        actions.updateFirstname(event.target.value);
    }

    updateLastname(event) {
        actions.updateLastname(event.target.value);
    }

    submitForm(event) {
        event.preventDefault();
        actions.submitForm();
    }

    render() {
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
                <div className="">
                    {this.state.message}
                </div>
                <LoadingPanel show={this.state.loading} />
            </form>
        );

    }

}

RegistrationForm.propTypes = {
    updateAuthority: React.PropTypes.func
};

export default RegistrationForm;