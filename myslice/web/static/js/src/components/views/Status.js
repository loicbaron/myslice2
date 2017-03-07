import React from 'react';

import store from '../../stores/views/Status';
import actions from '../../actions/views/Status';

import { View, ViewHeader, ViewBody, Panel } from '../base/View';
import Title from '../base/Title';

import { TestbedList } from '../objects/Testbed';
import { ResourceList } from '../objects/Resource';

class StatusView extends React.Component {

    constructor(props) {
        super(props);
        this.state = store.getState();
        this.onChange = this.onChange.bind(this);
    }

    componentDidMount() {
        store.listen(this.onChange);
        actions.getTestbeds();
    }

    componentWillUnmount() {
        store.unlisten(this.onChange);
    }

    onChange(state) {
        this.setState(state);
    }

    /* set the current testbed */
    setCurrentTestbed(testbed) {
        actions.setCurrentTestbed(testbed);
    }


    render() {
        let panelRight = null;
        let currentTestbedName = null;

        if (this.state.errorMessage) {
            return (
                <div>Something is wrong</div>
            );
        }

        if (this.state.currentTestbed) {
            panelRight = <ResourceList resources={this.state.resources} />;
            currentTestbedName = this.state.currentTestbed.name;
        }

        return (
            <View>
                <ViewHeader>
                    <Title title="Service Status"
                           subtitle={currentTestbedName}
                           separator="/"
                    />
                </ViewHeader>
                <ViewBody>
                    <Panel>
                        <TestbedList testbeds={this.state.testbeds}
                                    handleSelect={this.setCurrentTestbed}
                                    current={this.state.currentTestbed} />
                    </Panel>
                    <Panel>
                        {panelRight}
                    </Panel>
                </ViewBody>
            </View>
        );
    }
}

export default StatusView;