import React from 'react';

import PasswordInput from './PasswordInput';

class PasswordValidator extends React.Component {

    constructor(props){
        super(props);

        this.state = {
            "newPassword"    : "",
            "repeatPassword" : "", 
            "isSame"         : false
        };
        
        this.updateNewPassword = this.updateNewPassword.bind(this);
        this.updateRepeatPassword =this.updateRepeatPassword.bind(this);
        this.samePassword = this.samePassword.bind(this);
    }
    
    samePassword() {
        if (this.state.newPassword === this.state.repeatPassword){
            this.props.validatedPassword(this.state.newPassword);
            this.state.isSame = true;
            this.props.isSamePassword(this.state.isSame);
            this.forceUpdate();
        } else {
            this.state.isSame = false;
            this.props.isSamePassword(this.state.isSame);
            this.forceUpdate();
        }

    }

    updateNewPassword(password){
        this.state.newPassword = password;
        this.samePassword();
    }

    updateRepeatPassword(password){
        this.state.repeatPassword = password;
        this.samePassword();
    }

    render() {
            let message =   <span id="WarningMessage" className="WarningBlock">
                                {(this.state.isSame) ? "" : this.props.helpMessage}
                            </span>
            
            return (
                
                <div>
                    <PasswordInput  placeholder="New Password" 
                                    name="new_password"
                                    showPattern={this.props.showPattern}
                                    checkedPassword={this.updateNewPassword}
                                    description="New Password"
                                    correct={this.state.isSame}
                                    />
                    <PasswordInput  placeholder="Repeat Password" 
                                    name="repeat_password"
                                    showPattern={this.props.showPattern}
                                    checkedPassword={this.updateRepeatPassword}
                                    description="Repeat Password"
                                    correct={this.state.isSame}
                                    />
                    {message}
                </div>
            );
        }

}

PasswordInput.propTypes = {
    showPattern: React.PropTypes.bool,
    validatedPassword : React.PropTypes.func,
    isSamePassword: React.PropTypes.func
}

PasswordInput.defaultProps = {
    showPattern: true,
    validatedPassword: null
}

export default PasswordValidator;