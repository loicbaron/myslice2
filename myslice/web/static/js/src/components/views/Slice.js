import React from 'react';

import store from '../../stores/views/Slice';
import actions from '../../actions/views/Slice';

import View from '../base/View';
import { Panel, PanelHeader, PanelBody } from '../base/Panel';
import { UsersSectionSimple } from '../sections/User';
import Title from '../base/Title';
import Text from '../base/Text';
import DateTime from '../base/DateTime';

import SelectResourceDialog from '../dialogs/SelectResource';


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
            case 'users':
                dialog = <UsersDialog close={this.closeDialog} />;
                break;

        }


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
                        <ul>
                        {
                            this.state.testbeds.filter(function(testbed) {
                                return testbed.type == 'AM';
                            }).map(function(testbed) {
                                    return <li key={testbed.id} onClick={() => this.addResources(testbed)}>{testbed.name}</li>;
                            }.bind(this))
                        }
                        </ul>
                    </PanelBody>
                    {dialog}
                </Panel>

            </View>
        );
    }

}

export default SliceView;