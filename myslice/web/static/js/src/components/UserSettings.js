import React from 'react';
import ReactDOM from 'react-dom';
import {Tab, Tabs, TabList, TabPanel} from 'react-tabs';

import UserProfile from './UserProfile';
import UserAuthentication from './UserAuthentication';

class UserSettings extends React.Component {

    constructor(props) {
        super(props);
    }

    handleSelect(index, last) {
        console.log('Selected tab: ' + index + ', Last tab: ' + last);

    }

    render () {
        return (
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
                
        );
    }

}

export default UserSettings;

/*

*/
