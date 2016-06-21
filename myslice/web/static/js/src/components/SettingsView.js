import React from 'react';

import View from './base/View';
import Panel from './base/Panel';
import PanelHeader from './base/PanelHeader';
import PanelBody from './base/PanelBody';
import PanelMenu from './base/PanelMenu';
import PanelMenuEntry from './base/PanelMenuEntry';
import Title from './base/Title';

import actions from '../actions/SettingsActions'
import store from '../stores/SettingsStore'

import LoadingPanel from './LoadingPanel'
import SettingsProfile from './SettingsProfile';
import SettingsSsh from './SettingsSsh';

class SettingsView extends React.Component {

    constructor(props) {
        super(props);
        this.state = store.getState();
        this.handleSelect = this.handleSelect.bind(this);
        this.onChange = this.onChange.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
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

    onSubmit() {
        actions.onSubmit();
    }

    generateKeys() {
        actions.generateKeys();
    }

    handleSelect(name) {
        this.setState({
            'menuSelected' : name
        })
    }

    render () {

        var menuElement = (
            <PanelMenu>
                <PanelMenuEntry icon="user" name="profile" handleSelect={this.handleSelect}>
                    Profile
                </PanelMenuEntry>
                <PanelMenuEntry icon="key" name="ssh" handleSelect={this.handleSelect}>
                    SSH Keys
                </PanelMenuEntry>
                <PanelMenuEntry icon="unlock-alt" name="password" handleSelect={this.handleSelect}>
                    Password
                </PanelMenuEntry>
            </PanelMenu>
        );

        var panel = '';

        switch(this.state.menuSelected) {
            default:
            case 'profile':
                panel = (<Panel>
                    <PanelHeader>
                        <Title title="Profile" />
                    </PanelHeader>
                    <PanelBody>
                        <SettingsProfile profile={this.state.settings}
                                         onSubmit={this.onSubmit}
                            />
                        <LoadingPanel show={this.state.loading}/>
                    </PanelBody>
                </Panel>);
                break;
            case 'ssh':
                panel = (<Panel>
                    <PanelHeader>
                        <Title title="SSH" />
                    </PanelHeader>
                    <PanelBody>
                        <SettingsSsh generateKeys={this.generateKeys.bind(this)}
                                     public_key={this.state.settings.public_key}
                                     private_key={this.state.settings.private_key}
                                     />            
                        <LoadingPanel show={this.state.loading}/>
                    </PanelBody>
                </Panel>);
                break;
        }

        return (

            <View>
                {menuElement}
                {panel}
            </View>
            
                
        );
    }

}

export default SettingsView;