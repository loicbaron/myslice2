import React from 'react';
import UserProfileStore from '../stores/UserProfileStore';
import UserProfileActions from '../actions/UserProfileActions';
import AuthorityName from './AuthorityName';
import LoadingPanel from './LoadingPanel';

export default class UserProfile extends React.Component {

    constructor(props) {
        super(props);
        this.state = UserProfileStore.getState();
        this.onChange = this.onChange.bind(this);
    }

    componentDidMount() {
        UserProfileStore.listen(this.onChange);
        UserProfileActions.initUser();
    }

    componentWillUnmount() {
        UserProfileStore.unlisten(this.onChange);
    }
    
    // listen to the Store once something changes
    onChange(state) {
        this.setState(state);
    }

    // change the state and view
    updateLastname(event) {
        UserProfileActions.updateLastname(event.target.value);
    }

    updateFirstname(event) {
        UserProfileActions.updateFirstname(event.target.value);
    }

    updateBio(event) {
        UserProfileActions.updateBio(event.target.value);
    }

    updateUrl(event) {
        UserProfileActions.updateUrl(event.target.value);
    }

    submitForm(event) {
        event.preventDefault();
        UserProfileActions.onSubmit();
    }

    render() {

        return (
            <div>
                <h3> Your Details</h3>
                <form onSubmit={this.submitForm}>
                    <div>
                        <input  value={this.state.first_name} 
                                placeholder="First name" 
                                type="text" 
                                name="first_name"
                                onChange={this.updateFirstname.bind(this)}
                                />
                    </div>
                    <div>
                        <input  value={this.state.last_name} 
                                placeholder="Last name" 
                                type="text" 
                                name="last_name"
                                onChange={this.updateLastname.bind(this)}
                                />
                    </div>
                    <div>
                        <input  value={this.state.email} 
                                name="email"
                                placeholder="Email address"
                                type="text"
                                />
                    </div>
                    <AuthorityName id={this.state.authority} />
                    <div>
                        <input  value={this.state.bio}
                                placeholder="Bio"
                                type="text"
                                name="bio"
                                onChange={this.updateBio.bind(this)}
                                />
                    </div>
                    <div>
                        <input  value={this.state.url}
                                placeholder="Your Url"
                                type="text"
                                name="url"
                                onChange={this.updateUrl.bind(this)}
                                />
                    </div>
                    
                    <button type="submit" className="btn btn-default">Update Profile</button>  
                </form>
                <LoadingPanel show={this.state.loading} />
            </div>
            )
    }


}