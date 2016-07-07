import React from 'react';

import View from './base/View';
import Panel from './base/Panel';
import PanelHeader from './base/PanelHeader';
import PanelBody from './base/PanelBody';
import Title from './base/Title';
import Button from './base/Button';

import ActivityList from './ActivityList';
import RequestsList from './RequestsList';

class ActivityView extends React.Component {

    constructor(props) {
        super(props);
    }

    render() {

        return (
            <View>
                <Panel>
                    <PanelHeader>
                        <Title title="Activity" />
                    </PanelHeader>
                    <PanelBody>
                        <ActivityList />
                    </PanelBody>
                </Panel>
                <Panel>
                    <PanelHeader>
                        <Title title="Requests" />
                    </PanelHeader>
                    <PanelBody>
                        <RequestsList />
                    </PanelBody>
                </Panel>
            </View>
        );
    }
}

export default ActivityView;