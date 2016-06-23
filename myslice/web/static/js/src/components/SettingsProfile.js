import React from 'react';

import AuthorityName from './AuthorityName';
import Avatar from 'react-avatar';

class SettingsProfile extends React.Component {

    constructor(props) {
        super(props);
        this.state = {  "email"      : "",
                        "first_name" : "",
                        "last_name"  : "",
                        "authority"  : "",
                        "bio"        : "",
                        "url"        : "",
        }
    }

    componentDidMount() {
        if (this.props.profile) {
            this.setState(this.props.profile);
        }
    }

    componentWillReceiveProps(nextProps) {
        if (nextProps.profile) {
            this.setState(nextProps.profile);
        }
    }
    
    // The fields in Default Store is empty string
    handleChange(event) {
        this.setState({[event.target.name] : event.target.value})
    }

    submitForm(event) {
        event.preventDefault();
        this.props.submitProfile(this.state);
    }

    render() {
        let name = [this.state.first_name, this.state.last_name].join(' ');

        return (
            <div>
                <Avatar className="avatar" email={this.state.email} name={name} round={true} />
                <form onSubmit={this.submitForm.bind(this)}>
                    <div>
                        <input  value={this.state.first_name} 
                                placeholder="First name" 
                                type="text" 
                                name="first_name"
                                onChange={this.handleChange.bind(this)}
                                />
                    </div>
                    <div>
                        <input  value={this.state.last_name} 
                                placeholder="Last name" 
                                type="text" 
                                name="last_name"
                                onChange={this.handleChange.bind(this)}
                                />
                    </div>
                    <div>
                        <input  value={this.state.email} 
                                name="email"
                                placeholder="Email address"
                                type="text"
                                readOnly
                                />
                    </div>
                    <div>
                        <AuthorityName id={this.state.authority} />
                    </div>
                    <div>
                        <input  value={this.state.bio}
                                placeholder="Bio"
                                type="text"
                                name="bio"
                                onChange={this.handleChange.bind(this)}
                                />
                    </div>
                    <div>
                        <input  value={this.state.url}
                                placeholder="Your Url"
                                type="text"
                                name="url"
                                onChange={this.handleChange.bind(this)}
                                />
                    </div>
                    <button type="submit" className="btn btn-default">Update Profile</button>  
                </form>
            </div>
            )
    }

}

export default SettingsProfile;