import React from 'react';

import List from './base/List';
import Title from './base/Title';
import { AuthorityList } from'./objects/Authority';
import { ProjectList } from'./objects/Project';

import AuthorityName from './AuthorityName';
import Avatar from 'react-avatar';

class SettingsRights extends React.Component {

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
        console.log(this.props.profile);
        let name = [this.props.profile.first_name, this.props.profile.last_name].join(' ');
        var projectsElement;
        if(this.props.profile.projects){
            projectsElement = <div><Title title="Projects" /><ProjectList projects={this.props.profile.projects} /></div>
        }
        var authoritiesElement;
        if(this.props.profile.pi_authorities){
            authoritiesElement = <div><Title title="Authorities" /><AuthorityList authorities={this.props.profile.pi_authorities} /></div>
        }
        return (
            <div className="container-fluid">
                <div className = "row">
                    <div className="col-md-8 col-md-offset-2">
                        <div className="settings-group profileAvatar">
                            <Avatar className="avatar" email={this.props.profile.email} name={name} round={true} />
                            {authoritiesElement}
                            {projectsElement}
                        </div>
                    </div>
                </div>
            </div>
            )
    }

}

SettingsRights.propTypes = {
    submitProfile: React.PropTypes.func,
    updateProfile: React.PropTypes.func
}

export default SettingsRights;
