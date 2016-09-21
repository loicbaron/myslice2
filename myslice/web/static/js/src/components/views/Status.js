import React from 'react';

import store from '../../stores/views/Status';
import actions from '../../actions/views/Status';

import View from '../base/View';
import Panel from '../base/Panel';
import PanelHeader from '../base/PanelHeader';
import PanelBody from '../base/PanelBody';
import Title from '../base/Title';

import TestbedsList from '../objects/TestbedList';
import ResourceList from '../objects/ResourceList';

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
        console.log('current testbed = ');
        console.log(testbed);
        actions.setCurrentTestbed(testbed);
    }


    render() {
        var panelRight = null;

        if (this.state.errorMessage) {
            return (
                <div>Something is wrong</div>
            );
        }

        if (this.state.currentTestbed) {

            panelRight = <Panel>
                <PanelHeader>
                    <Title title={this.state.currentTestbed.name} subtitle={this.state.currentTestbed.hostname} />
                </PanelHeader>
                <PanelBody>
                    <ResourceList resources={this.state.resources} />
                </PanelBody>
            </Panel>;

        }

        return (
            <View>
                <Panel>
                    <PanelHeader>
                        <Title title="Service Status" subtitle="" />
                    </PanelHeader>
                    <PanelBody>
                        <TestbedsList testbeds={this.state.testbeds} setCurrent={this.setCurrentTestbed} current={this.state.currentTestbed} />
                    </PanelBody>
                </Panel>
                {panelRight}
            </View>
        );
    }
}

export default StatusView;