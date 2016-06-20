import React from 'react';

import View from './base/View';
import Panel from './base/Panel';
import PanelHeader from './base/PanelHeader';
import PanelBody from './base/PanelBody';
import PanelMenu from './base/PanelMenu';
import PanelMenuEntry from './base/PanelMenuEntry';
import Title from './base/Title';

import SettingsProfile from './SettingsProfile';
import SettingsSsh from './SettingsSsh';

class SettingsView extends React.Component {

    constructor(props) {
        super(props);
        this.state ={
            'menuSelected' : 'profile'
        };
        this.handleSelect = this.handleSelect.bind(this)
    }

    handleSelect(name) {
        console.log(name)
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
                        <SettingsProfile />
                    </PanelBody>
                </Panel>);
                break;
            case 'ssh':
                panel = (<Panel>
                    <PanelHeader>
                        <Title title="SSH" />
                    </PanelHeader>
                    <PanelBody>
                        <SettingsSsh />
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

/*
<Tabs onSelect={this.handleSelect} SelectedIndex={2}>
                    <TabList>
                        <Tab> Profile </Tab>
                        <Tab> Authentication </Tab>
                        <Tab> Account </Tab>
                        <Tab> xxxx </Tab>
                    </TabList>

                    <TabPanel>
                        <UserProfile />
                    </TabPanel>
                    <TabPanel>
                        <UserAuthentication />
                    </TabPanel>
                    <TabPanel>
                        <h2>Hello from Baz</h2>
                    </TabPanel>
                    <TabPanel>
                        <h2>Hello from Baz</h2>
                    </TabPanel>

                </Tabs>
 */
export default SettingsView;