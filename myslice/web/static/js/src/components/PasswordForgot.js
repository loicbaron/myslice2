import React from 'react';

import actions from '../actions/PasswordActions'
import store from '../stores/PasswordStore'

import EmailInput from './EmailInput';

class PasswordForgot extends React.Component {

    constructor(props) {
        super(props);
        this.state = store.getState();
        this.onChange = this.onChange.bind(this);
    }

    componentDidMount() {
        store.listen(this.onChange);
    }

    componentWillUnmount(){
        store.unlisten(this.onChange);
    }

    onChange(state) {
        this.setState(state);
    }

    onChangeEmail(value) {
        actions.updateEmail(value);
    }

    submitForm(e){
        e.preventDefault();
        actions.submitEmail();
    }

    render () {
        let content;
        if(this.state.sent){
            document.getElementById("message").style.display="none";
            content = (
                <div>An email has been sent, follow the link to reset your password.</div>
            )
        }else{
            content = (
                <div className="col-sm-8">
                <form onSubmit={this.submitForm}>
                    <div>
                        <EmailInput handleChange={this.onChangeEmail}/>
                    </div>
                    <button type="submit" className="btn btn-default">Reset my password</button>  
                </form>
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

export default PasswordForgot;
