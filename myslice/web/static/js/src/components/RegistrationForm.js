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
        if (this.state.success) {
            return (
                <div>
                    Success!
                </div>
            );
        } else {

            return (
                <form onSubmit={this.submitForm}>
                    <div className="row">
                        <div className="col-sm-4 col-sm-offset-4 inputForm">
                            <AuthoritiesSelect handleChange={this.updateAuthority}/>
                        </div>
                    </div>
                    <div className="row">
                        <div className="col-sm-7 col-sm-offset-3">
                            <p className="inputDescription">
                                Choose your organization (company or university) from this list.<br />
                                Use the arrow keys to scroll through the list; type part of the name to narrow down the list.
                            <br />
                               <b>We will send an email to the managers</b> that we have on record for your organization,
                                asking them to validate your sign-up request.
                            </p>
                        </div>
                    </div>
                    <div className="row">
                        <div className="col-sm-4 col-sm-offset-4 inputForm">
                            <EmailInput handleChange={this.updateEmail}/>
                        </div>
                    </div>
                    <div className="row">
                        <div className="col-sm-7 col-sm-offset-3">
                            <p className="inputDescription">
                                Please provide your Email address, it will be your identifier for logging in. <br />
                                We will also contact you to verify your account and occasionally for important communications.
                            </p>
                        </div>
                    </div>
                    <div className="row">
                        <div className="col-sm-4 col-sm-offset-4 inputForm">
                            <input onChange={this.updateFirstname} placeholder="First name" type="text" name="firstname"/>
                        </div>
                    </div>
                    <div className="row">
                        <div className="col-sm-4 col-sm-offset-4 inputForm">
                            <input onChange={this.updateLastname} placeholder="Last name" type="text" name="lastname"/>
                        </div>
                    </div>
                    <div className="row">
                        <div className="col-sm-4 col-sm-offset-4 inputForm">
                            <input type="checkbox" name="terms" />&nbsp;&nbsp; I agree to the&nbsp;
                            <a href="#" data-toggle="modal" data-target="#myModal">terms and conditions.</a>
                        </div>
                    </div>
                    <div className="row">
                        <div className="col-sm-4 col-sm-offset-4 inputSubmit">
                            <input type="submit" className="btn btn-default"/>
                        </div>
                    </div>

                    <div className="row">
                        <div className="col-sm-4 col-sm-offset-4">
                            {this.state.message}
                        </div>
                    </div>
                    <LoadingPanel show={this.state.loading}/>
                </form>
            );
        }

    }

}

RegistrationForm.propTypes = {
    updateAuthority: React.PropTypes.func
};

export default RegistrationForm;