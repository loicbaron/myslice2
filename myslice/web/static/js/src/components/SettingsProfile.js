import React from 'react';

import AuthorityName from './AuthorityName';
import Avatar from 'react-avatar';

class SettingsProfile extends React.Component {

    constructor(props) {
        super(props);
    }
    
    // The fields in Default Store is empty string
    handleChange(event) {
        this.props.updateProfile(event.target.name, event.target.value)
    }

    submitForm(event) {
        event.preventDefault();
        this.props.submitProfile(this.state);
    }

    render() {
        //let name = [this.props.profile.first_name, this.props.profile.last_name].join(' ');

        return (
            <div>
                <Avatar className="avatar" email={this.props.profile.email} name={name} round={true} />
                <form onSubmit={this.submitForm.bind(this)}>
                    <div>
                        <input  value={this.props.profile.first_name} 
                                placeholder="First name" 
                                type="text" 
                                name="first_name"
                                onChange={this.handleChange.bind(this)}
                                />
                    </div>
                    <div>
                        <input  value={this.props.profile.last_name} 
                                placeholder="Last name" 
                                type="text" 
                                name="last_name"
                                onChange={this.handleChange.bind(this)}
                                />
                    </div>
                    <div>
                        <input  value={this.props.profile.email} 
                                name="email"
                                placeholder="Email address"
                                type="text"
                                readOnly
                                />
                    </div>
                    <div>
                        <AuthorityName id={this.props.profile.authority} />
                    </div>
                    <div>
                        <input  value={this.props.profile.bio}
                                placeholder="Bio"
                                type="text"
                                name="bio"
                                onChange={this.handleChange.bind(this)}
                                />
                    </div>
                    <div>
                        <input  value={this.props.profile.url}
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

SettingsProfile.propTypes = {
    profile: React.PropTypes.object,
    submitProfile: React.PropTypes.func,
    updateProfile: React.PropTypes.func.isRequired
}

export default SettingsProfile;