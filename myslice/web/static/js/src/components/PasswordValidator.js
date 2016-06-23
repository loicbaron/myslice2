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
            this.forceUpdate();
        } else {
            this.state.isSame = false;
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

            let message = <div> {(this.state.isSame) ? "Same Password" : ""} </div>
            
            return (
                <div>
                    <PasswordInput  placeholder="New Password" 
                                    name="new_password"
                                    showPattern={this.props.showPattern}
                                    checkedPassword={this.updateNewPassword}
                                    />
                    <PasswordInput  placeholder="Repeat Password" 
                                    name="repeat_password"
                                    showPattern={this.props.showPattern}
                                    checkedPassword={this.updateRepeatPassword}
                                    />
                    {message}
                </div>
            );
        }

}

PasswordInput.propTypes = {
    showPattern: React.PropTypes.bool,
    showSameMessage: React.PropTypes.bool,
    validatedPassword : React.PropTypes.func,
}

PasswordInput.defaultProps = {
    showPattern: true,
    showSameMessage: true,
    validatedPassword: null
}

export default PasswordValidator;