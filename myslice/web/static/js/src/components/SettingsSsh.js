import React from 'react';

import Button from './base/Button';
import DownloadButton from './DownloadButton';

export default class UserAuthentication extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            "public_key"   : "",
            "private_key"  : "",
        }
    }

    generateKeys() {
        console.log('generateKeys');
        this.props.generateKeys();
    }

    downloadPublicKeys() {
        return {
            mime: 'text/plain',
            filename:'publickey',
            contents: this.props.public_key,
        }
    }

    downloadPrivateKeys() {
        return {
            mime: 'text/plain',
            filename:'privatekey',
            contents: this.props.private_key
        }

    }

    submitForm(event) {
        event.preventDefault();
    }

    render() {

        return (
                <div>
                    {this.state.message}
                    <Button label="Generate New Keys" handleClick={this.generateKeys.bind(this)}/> 
                    <DownloadButton 
                            downloadTitle="Download Pubic Keys" 
                            genFile={this.downloadPublicKeys.bind(this)}
                            /> 
                    <DownloadButton 
                            downloadTitle="Download Private Keys" 
                            genFile={this.downloadPrivateKeys.bind(this)}
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