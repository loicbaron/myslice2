import React from 'react';

import PasswordInput from './PasswordInput';

class SettingsPassword extends React.Component {

    constructor(props) {
        super(props)
    }

    render() { 

        return (
                <form onSubmit={this.submitForm}>
                    <div>
                        <PasswordInput  placeholder="Old Password"
                                        name="old_passwod"
                                        showPattern={false}
                                /> 
                        <PasswordInput  placeholder="New Password" 
                                        name="new_password"
                                        showPattern={true}
                                />
                        <PasswordInput  placeholder="Repeat Password" 
                                        name="repeat_password"
                                        showPattern={true}
                                />

                    </div>
                    <button type="submit" className="btn btn-default">Reset</button>
                </form> 
        );
    }

}

export default SettingsPassword;