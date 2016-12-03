import React from 'react';

import store from '../../stores/views/Slice';
import actions from '../../actions/views/Slice';

import View from '../base/View';
import { Panel, PanelHeader, PanelBody } from '../base/Panel';
import { UsersSectionSimple } from '../sections/User';
import Title from '../base/Title';
import Text from '../base/Text';
import DateTime from '../base/DateTime';

import { TestbedSectionPanel } from '../sections/Testbed';

import SelectResourceDialog from '../dialogs/SelectResource';
import SelectUserDialog from '../dialogs/SelectUser';

class SliceView extends React.Component {

    constructor(props) {
        super(props);
        this.state = store.getState();
        this.onChange = this.onChange.bind(this);
        this.closeDialog = this.closeDialog.bind(this);
    }

    componentDidMount() {
        store.listen(this.onChange);
        actions.fetchSlice(this.props.slice);
        actions.fetchTestbeds();
    }

    componentWillUnmount() {
        store.unlisten(this.onChange);
    }

    onChange(state) {
        this.setState(state);
    }

    closeDialog() {
        actions.closeDialog();
    }

    addResources(testbed) {
        actions.selectResourceDialog(testbed);
    }

    addUser() {
        actions.selectUserDialog();
    }
    
    render() {
        var panelRight = null;
        var dialog = null;

        if (this.state.errorMessage) {
            return (
                <div>Something is wrong</div>
            );
        }

        switch(this.state.dialog) {
            case 'selectResource':
                dialog = <SelectResourceDialog testbed={this.state.testbed} close={this.closeDialog} />;
                break;
            case 'selectUser':
                dialog = <SelectUserDialog cancel={this.closeDialog} />;
                break;

        }


        /*
        *  Define options for testbed panel
        * */

        let testbedListOptions = [
            {
                'label' : 'Add Resources',
                'icon' : 'add',
                'callback' : this.addResources
            }
        ];

        return (
            <View>
                <Panel>
                    <PanelHeader>
                        <Title title={this.state.slice.name || this.state.slice.shortname || ''} />
                    </PanelHeader>
                    <PanelBody>
                        <div>
                            <p>
                                {this.state.slice.id}
                            </p>

                            <DateTime label="Created" timestamp={this.state.slice.created} />
                            <DateTime label="Enabled" timestamp={this.state.slice.enabled} />
                            <DateTime label="Last updated" timestamp={this.state.slice.updated} />

                        </div>
                        <UsersSectionSimple users={this.state.slice.users} />
                    </PanelBody>
                </Panel>
                <Panel>
                    <PanelHeader>

                    </PanelHeader>
                    <PanelBody>
                        <Text>
                            Please select the resources to reserve by choosing a Testbed (text to change)
                        </Text>
                        <br />
                        <TestbedSectionPanel testbeds={this.state.testbeds} listOptions={testbedListOptions} />
                    </PanelBody>
                    {dialog}
                </Panel>

            </View>
        );
    }

}

export default SliceView;
