import React from 'react';
import store from '../stores/UserAuthenticationStore';
import actions from '../actions/UserAuthenticationActions';
import Button from './base/Button';
import DownloadButton from './DownloadButton';

export default class UserAuthentication extends React.Component {

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

    // listen to the Store once something changes
    onChange(state) {
        this.setState(state);
    }

/*   // change the state and view
    updateLastname(event) {
        actions.updateLastname(event.target.value);
    }

    updateFirstname(event) {
        actions.updateFirstname(event.target.value);
    }

    updateBio(event) {
        actions.updateBio(event.target.value);
    }

    updateUrl(event) {
        actions.updateUrl(event.target.value);
    }
*/
    generateNewKeys() {
        console.log('generateKeys');
        actions.generateKeys();
    }

    downloadPublicKeys() {
        actions.fetchProfile();
        return {
            mime: 'text/plain',
            filename:'publickey',
            contents: this.state.public_key,
        }
    }

    downloadPrivateKeys() {
        actions.fetchProfile();
        return {
            mime: 'text/plain',
            filename:'privatekey',
            contents: this.state.private_key,
        }

    }

    submitForm(event) {
        event.preventDefault();
    }

    render() {

        return (
                <div>
                    {this.state.message}
                    <Button label="Generate New Keys" handleClick={this.generateNewKeys.bind(this)}/> 
                    <DownloadButton 
                            downloadTitle="Download Pubic Keys" 
                            genFile={this.downloadPublicKeys.bind(this)}
                            /> 
                    <DownloadButton 
                            downloadTitle="Download Private Keys" 
                            genFile= {this.downloadPrivateKeys.bind(this)} 
                            />
                    <form onSubmit={this.submitForm}>
                        <div>
                            <input  defaultvalue=''
                                    placeholder="Current Password" 
                                    type="text" 
                                    name="current_password"
                                    />
                            <input  defaultvalue=''
                                    placeholder="New Password" 
                                    type="text" 
                                    name="new_password"
                                    />
                            <input  defaultvalue=''
                                    placeholder="Repeat Password" 
                                    type="text" 
                                    name="repeat_password"
                                    />
                        </div>
                        
                        <button type="submit" className="btn btn-default">Reset</button>  
                    </form>
                </div>
            );
    }

}