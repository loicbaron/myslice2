import React from 'react';
import ReactDOM from 'react-dom';
import {Tab, Tabs, TabList, TabPanel} from 'react-tabs';
import UserProfile

class UserAccount extends React.Component {

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
                    </TabList>

                    <TabPanel>
                        <h2>Hello from Foo</h2>
                    </TabPanel>
                        <TabPanel>
                    <h2>Hello from Bar</h2>
                        </TabPanel>
                    <TabPanel>
                        <h2>Hello from Baz</h2>
                    </TabPanel>



                </Tabs>
        );
    }

}