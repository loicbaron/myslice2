import React from 'react';

import store from '../../stores/views/Slice';
import actions from '../../actions/views/Slice';

import { View, ViewHeader, ViewBody, Panel  } from '../base/View';
import { UsersSummary } from '../objects/User';
import { ResourcesSummary } from '../objects/Resource';
import Title from '../base/Title';
import Text from '../base/Text';
import DateTime from '../base/DateTime';

import { TestbedSectionPanel } from '../sections/Testbed';
import { ResourceList } from '../objects/Resource';

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

    /*
        Shows the add resources dialog for the selected testbed
     */
    selectResourceDialog(testbed) {
        actions.selectResourceDialog(testbed);
    }

    /*
        Once user select some resources and apply this wil be called.
     */
    addResources(resources, lease={}) {
        actions.saveSlice({'resources': resources, 'lease': lease})
    }

    renderSliceTitle() {
        return this.state.slice.name || this.state.slice.shortname || ''
    }
    renderSliceProjectTitle() {
        if (this.state.slice.project) {
            return this.state.slice.project.name || this.state.slice.project.shortname
        }
    }
    
    render() {
        let dialog = null;

        if (this.state.errorMessage) {
            return (
                <div>Something is wrong</div>
            );
        }

        switch(this.state.dialog) {
            case 'selectResource':
                dialog = <SelectResourceDialog testbed={this.state.testbed} apply={this.addResources} cancel={this.closeDialog} />;
                break;

        }
        console.log(this.state.slice);

        /*
        *  Define options for testbed panel
        * */

        let testbedListOptions = [
            {
                'label' : 'Add Resources',
                'icon' : 'add',
                'callback' : this.selectResourceDialog
            }
        ];
        console.log(this.state.slice);

        return (<View>
            <ViewHeader>
                <Title
                    title={this.renderSliceProjectTitle()}
                    subtitle={this.renderSliceTitle()}
                    separator="/"
                />
            </ViewHeader>
            <ViewBody>
                <Panel>
                    <div>
                        <p>
                            {this.state.slice.id}
                        </p>
                        <DateTime label="Created" timestamp={this.state.slice.created} />
                        <DateTime label="Last updated" timestamp={this.state.slice.updated} />
                    </div>
                    <ResourcesSummary resources={this.state.slice.resources} />
                    <UsersSummary users={this.state.slice.users} />
                </Panel>
                <Panel>
                    <Text>
                        Please select the resources to reserve by choosing a Testbed (text to change)
                    </Text>
                    <br />
                    <TestbedSectionPanel testbeds={this.state.testbeds} listOptions={testbedListOptions} />
                </Panel>
            </ViewBody>
            {dialog}
        </View>);
    }

}

export default SliceView;
