import React from 'react';

import actions from '../actions/PasswordActions'
import store from '../stores/PasswordStore'

class PasswordReset extends React.Component {

    constructor(props) {
        super(props);
        this.state = store.getState();
        this.onChange = this.onChange.bind(this);
        this.onChangeRepeate = this.onChangeRepeate.bind(this);
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

    onChangePassword(e) {
        actions.updatePassword(e.target.value);
    }
    onChangeRepeate(e) {
        if (e.target.value != this.state.password){
            actions.errorupdatePassword();
        }else{
            actions.matchingPassword();
        }
    }

    submitForm(e){
        e.preventDefault();
        actions.onSubmit();
    }

    render () {

        return (
            <div>
                <form onSubmit={this.submitForm}>
                    <div>
                        <input  defaultvalue=''
                                placeholder="New Password" 
                                type="text" 
                                name="new_password"
                                onChange={this.onChangePassword}
                                />
                        <input  defaultvalue=''
                                placeholder="Repeat Password" 
                                type="text" 
                                name="repeat_password"
                                onChange={this.onChangeRepeate}
                                />
                    </div>
                    <button type="submit" className="btn btn-default">Save</button>  
                </form>
            </div>
        );
    }

}

export default PasswordReset;
