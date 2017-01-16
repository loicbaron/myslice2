
var React = require('react');
import actions from '../actions/RegistrationActions';
import store from '../stores/RegistrationStore';
import AuthoritiesSelect from './forms/SelectAuthority';
import EmailInput from './EmailInput';
import InputText from './InputText';
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
        console.log("changed");
        this.setState(state);
    }
    updateAuthority(value) {
        actions.updateAuthority(value);
    }

    updateEmail(value) {
        actions.updateEmail(value);
    }
    updatePassword(value) {
        actions.updatePassword(value);
    }
    updateFirstname(value) {
        actions.updateFirstname(value);
    }
    updateLastname(value) {
        actions.updateLastname(value);
    }
    updateTerms(event) {
        actions.updateTerms(event.target.value);
    }

    submitForm(event) {
        event.preventDefault();
        actions.submitForm();
    }

    render() {
        if (this.state.success) {
            return (
                <div className="col-sm-6 col-sm-offset-3">

                </div>
            );
        } else {
            /*
            Regular Expression for Names (firstname, lastname)
            ^[a-zA-ZÀ-ÿ]{1}(?!.*([\s\’\'-])\1)[a-zA-ZÀ-ÿ\s\’\'-]{0,50}[a-zA-ZÀ-ÿ]{1}$


            Regular Expression for emails
            ^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$

            */

    	    var emailRegExp = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
            var errorMessage = '';
            if(this.state.errorMessage){
                errorMessage = <div className="row">
                    <div className="col-sm-4 col-sm-offset-4 alert alert-danger">
                    {this.state.errorMessage}
                    </div>
                </div>
            }
            return (
                <form onSubmit={this.submitForm}>
                    {errorMessage}
                    <div className="row">

                        <div className="col-md-3">
                                <i className="fa fa-university" aria-hidden="true"></i>
                        </div>
                        <div className="col-sm-7">
                            <AuthoritiesSelect handleChange={this.updateAuthority}/>
                            <a href="/addOrganization">Add organization</a>
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
                        <InputText name="first_name" handleChange={this.updateFirstname} placeholder="Firstname" required={true} message="is required" />
                    </div>
                    <div className="row">
                        <InputText name="last_name" handleChange={this.updateLastname} placeholder="Lastname" required={true} message="is required" />
                    </div>
                    <div className="row">
                    <p>&nbsp;</p>
                    </div>
                    <div className="row">
                        <div className="col-sm-7 col-sm-offset-3">
                            <p className="inputDescription">
                                Please provide your Email address, it will be your identifier for logging in. <br />
                                We will also contact you to verify your account and occasionally for important communications.e
                            </p>
                        </div>
                    </div>
                    <div className="row">
                        <InputText name="email" handleChange={this.updateEmail} placeholder="Email address" regex={emailRegExp} message="Invalid email" />
                    </div>
                    <div className="row">
                        <InputText name="password" handleChange={this.updatePassword} placeholder="Password" regex=".{8,}$" message="must be at least 8 characters" type="password" />
                    </div>

                    <div className="row">
                        <div className="col-sm-4 col-sm-offset-4 inputForm">
                            <input type="checkbox" name="terms" onChange={this.updateTerms} />&nbsp;&nbsp; I agree to the&nbsp;
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
