import React from 'react';

import actions from '../actions/SettingsActions'
import store from '../stores/SettingsStore'
import SettingsPassword from './SettingsPassword';

class PasswordReset extends React.Component {

    constructor(props) {
        super(props);
        this.state = store.getState();
        this.onChange = this.onChange.bind(this);
    }

    componentDidMount() {
        store.listen(this.onChange);
        actions.updateHashing(this.props.new_hashing);
    }

    componentWillUnmount(){
        store.unlisten(this.onChange);
    }

    onChange(state) {
        this.setState(state);
    }

    updateNewpassword(newPassword){
        actions.updateNewpassword(newPassword);
    }

    submitResetPassword(){
        actions.submitResetPassword();
    }

    render () {
        let content;
        if(this.state.passwordUpdated){
            document.getElementById("message").style.display="none";
            content = (
                <div className="col-sm-6 col-sm-offset-1">Your password has been updated. <br/><br/> Please <a href="/">Login</a></div>
            )
        }else{
            content = (
            <div>
                 <SettingsPassword newPassword={this.updateNewpassword.bind(this)}
                                   submitPassword={this.submitResetPassword.bind(this)}
                 />   
            </div>
            )
        }
        return (
            <div className="row">
            {content}
            </div>
        );
    }

}

export default PasswordReset;
