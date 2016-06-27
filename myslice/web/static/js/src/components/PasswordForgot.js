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
        console.log(value);
        actions.updateEmail(value);
    }

    submitForm(e){
        console.log('click');
        e.preventDefault();
        actions.submitEmail();
    }

    render () {

        return (
            <div>
                <form onSubmit={this.submitForm}>
                    <div>
                        <EmailInput handleChange={this.onChangeEmail}/>
                    </div>
                    <button type="submit" className="btn btn-default">Reset my password</button>  
                </form>
            </div>
        );
    }

}

export default PasswordForgot;
