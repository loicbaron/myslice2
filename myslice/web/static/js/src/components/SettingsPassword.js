import React from 'react';

import PasswordValidator from './PasswordValidator';
import ElementIcon from './base/ElementIcon';

class SettingsPassword extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
                    "isSame" : false,
                    "helpMessage" : ""
                    }   
        this.inputOldPassword = this.inputOldPassword.bind(this);
        this.inputNewPassword = this.inputNewPassword.bind(this);
        this.isSamePassword = this.isSamePassword.bind(this);
    }   

    inputNewPassword(newPassword) {
        this.props.newPassword(newPassword);
    }

    inputOldPassword(event) {
        var oldPassword = event.target.value;
        this.props.oldPassword(oldPassword);
    }

    isSamePassword(status){
        this.state.isSame = status;
        this.state.helpMessage = "";
    }

    submitForm(event) {
        event.preventDefault();
        if (this.state.isSame) {
            this.props.submitPassword();
        } else {
            this.state.helpMessage = "Password don't match";
            this.forceUpdate()
        }
        
    }

    render() { 

        return (
            <div className="container-fluid">
                <div className = "row">
                    <div className="col-md-6 col-md-offset-3">
                        <form onSubmit={this.submitForm.bind(this)}>
                            <div className="settings-group">
                                <span className="settings-span">Old Password</span>
                                <input  placeholder="Old Password"
                                            name="oldPassword"
                                            type="password"
                                            onChange={this.inputOldPassword}
                                            />
                            </div>
                                <PasswordValidator 
                                        showPattern={true}
                                        validatedPassword={this.inputNewPassword}
                                        isSamePassword={this.isSamePassword}
                                        helpMessage= {this.state.helpMessage}
                                        />
                            <button type="submit" className="btn btn-default">Reset</button>
                        </form>
                    </div>
                </div>
            </div>
        );
    }

}


PasswordValidator.propTypes = {
    oldPassword: React.PropTypes.func,
    newPassword: React.PropTypes.func,
    submitPassword: React.PropTypes.func,
}

export default SettingsPassword;