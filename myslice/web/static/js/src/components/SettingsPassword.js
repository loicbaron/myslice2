import React from 'react';

import PasswordValidator from './PasswordValidator';

class SettingsPassword extends React.Component {

    constructor(props) {
        super(props);
        
        this.inputOldPassword = this.inputOldPassword.bind(this);
        this.inputNewPassword = this.inputNewPassword.bind(this);

    }   

    inputNewPassword(newPassword) {
        this.props.resetPassword(newPassword);
    }

    inputOldPassword(event) {
        var oldPassword = event.target.value;
        this.props.repeatPassword(oldPassword);
    }

    submitForm(event) {
        event.preventDefault();
        this.props.submitPassword();
    }

    render() { 

        return (
                <form onSubmit={this.submitForm.bind(this)}>
                        <input  placeholder="Old Password"
                                name="oldPassword"
                                type="password"
                                onChange={this.inputOldPassword}
                                />
                        <PasswordValidator 
                                showPattern={true}
                                validatedPassword={this.inputNewPassword}
                                />
                    <button type="submit" className="btn btn-default">Reset</button>
                </form> 
        );
    }

}


PasswordValidator.propTypes = {
    repeatPassword: React.PropTypes.func,
    resetPassword: React.PropTypes.func,
    submitPassword: React.PropTypes.func,
}

export default SettingsPassword;