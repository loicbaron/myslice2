import React from 'react';

import { View, ViewHeader, ViewBody, Panel, PanelMenu, PanelMenuEntry } from './base/View';
import Title from './base/Title';

import actions from '../actions/SettingsActions'
import store from '../stores/SettingsStore'

import LoadingPanel from './LoadingPanel'
import SettingsProfile from './SettingsProfile';
import SettingsRights from './SettingsRights';
import SettingsSsh from './SettingsSsh';
import SettingsPassword from './SettingsPassword';

class SettingsView extends React.Component {

    constructor(props) {
        super(props);
        this.state = store.getState();
        this.handleSelect = this.handleSelect.bind(this);
        this.onChange = this.onChange.bind(this);
    }

    componentDidMount() {
        store.listen(this.onChange);
        actions.fetchSettings();
    }

    componentWillUnmount(){
        store.unlisten(this.onChange);
    }

    onChange(state) {
        this.setState(state);
    }
    // for Profile
    submitProfile() {
        actions.submitProfile();
    }

    updateProfile(name, value) {
        actions.updateProfile(name, value);
    }

    // for Keys
    generateKeys() {
        actions.generateKeys();
    }

    // for Password
    updateOldpassword(oldPassword){
        actions.updateOldpassword(oldPassword);
    }

    updateNewpassword(newPassword){
        actions.updateNewpassword(newPassword);
    }

    submitPassword(){
        actions.submitPassword();
    }

    handleSelect(name) {
        actions.updateSelected(name);
    }

    renderUserName() {
        let user_name = null;
        if (this.state.profile.first_name) {
            user_name = this.state.profile.first_name;
        }
        if (this.state.profile.last_name) {
            user_name += ' ' + this.state.profile.last_name;
        }
        return user_name || this.state.profile.email || '';
    }

    render () {

        let panelMenu = (
            <PanelMenu>
                <PanelMenuEntry icon="user" name="profile" handleSelect={this.handleSelect}>
                    Profile
                </PanelMenuEntry>
                <PanelMenuEntry icon="institution" name="rights" handleSelect={this.handleSelect}>
                    Access rights
                </PanelMenuEntry>
                <PanelMenuEntry icon="key" name="ssh" handleSelect={this.handleSelect}>
                    SSH Keys
                </PanelMenuEntry>
                <PanelMenuEntry icon="unlock-alt" name="password" handleSelect={this.handleSelect}>
                    Password
                </PanelMenuEntry>
            </PanelMenu>
        );

        let panelMenuSelected = null;
        let panel = null;

        switch(this.state.menuSelected) {
            default:
            case 'profile':
                panel = <Panel>
                            <SettingsProfile profile={this.state.profile}
                                                 submitProfile={this.submitProfile.bind(this)}
                                                 updateProfile={this.updateProfile.bind(this)}
                                                />
                            <LoadingPanel show={this.state.loading}/>
                        </Panel>;
                break;
            case 'rights':
                panelMenuSelected = "Access rights";
                panel = <Panel>
                            <SettingsRights profile={this.state.profile}
                                                 submitProfile={this.submitProfile.bind(this)}
                                                 updateProfile={this.updateProfile.bind(this)}
                                                />
                            <LoadingPanel show={this.state.loading}/>
                        </Panel>;
                break;
            case 'ssh':
                panelMenuSelected = "SSH";
                panel = <Panel>
                            <SettingsSsh generateKeys={this.generateKeys.bind(this)}
                                         public_key={this.state.profile.public_key}
                                         private_key={this.state.profile.private_key}
                                         />
                            <LoadingPanel show={this.state.loading}/>
                        </Panel>;
                break;

            case 'password':
                panelMenuSelected = "Reset Password";
                panel = <Panel>
                            <SettingsPassword newPassword={this.updateNewpassword.bind(this)}
                                              oldPassword={this.updateOldpassword.bind(this)}
                                              submitPassword={this.submitPassword.bind(this)}
                                            />
                            <LoadingPanel show={this.state.loading}/>
                        </Panel>;
                break;

        }

        return (
            <View>
                <ViewHeader>
                    <Title
                        title={this.renderUserName()}
                        subtitle={panelMenuSelected}
                        separator="/"
                    />
                </ViewHeader>
                <ViewBody>
                    {panelMenu}
                    {panel}
                </ViewBody>
            </View>
            
                
        );
    }

}

export default SettingsView;
