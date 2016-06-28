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
        let name = [this.props.profile.first_name, this.props.profile.last_name].join(' ');

        return (
            <div className="container-fluid">
                <div className = "row">
                    <div className="col-md-8 col-md-offset-2">
                        <div className="settings-group profileAvatar">
                            <Avatar className="avatar" email={this.props.profile.email} name={name} round={true} />
                        </div>
                        <form onSubmit={this.submitForm.bind(this)}>
                            <div className="settings-group profileLastName ">
                                <span className="settings-span">First Name</span>

                                <input  value={this.props.profile.first_name} 
                                        placeholder="First name" 
                                        type="text" 
                                        name="first_name"
                                        onChange={this.handleChange.bind(this)}
                                        />
                            </div>
                            <div className="settings-group profileFirstName">
                                <span className="settings-span">Last Name</span>
                                <input  value={this.props.profile.last_name} 
                                        placeholder="Last name" 
                                        type="text" 
                                        name="last_name"
                                        onChange={this.handleChange.bind(this)}
                                        />
                            </div>
                            <div className="settings-group profileEmail">
                                <span className="settings-span">Email</span>
                                <input  value={this.props.profile.email} 
                                        name="email"
                                        placeholder="Email address"
                                        type="text"
                                        disabled
                                        />
                            </div>
                            <div className="settings-group profileAuthority">
                                <span className="settings-span">Authority</span>
                                <input  value={this.props.profile.authority.name} 
                                        name="authority"
                                        placeholder="Authority"
                                        type="text"
                                        disabled
                                        />
                            </div>
                            <div className="settings-group profileBio">
                                <span className="settings-span">Biography</span>
                                <input  value={this.props.profile.bio}
                                        placeholder="Biography"
                                        type="text"
                                        name="bio"
                                        onChange={this.handleChange.bind(this)}
                                        />
                            </div>
                            <div className="settings-group profileUrl">
                                <span className="settings-span">Your Url</span>
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
                </div>
            </div>
            )
    }

}

SettingsProfile.propTypes = {
    submitProfile: React.PropTypes.func,
    updateProfile: React.PropTypes.func
}

export default SettingsProfile;