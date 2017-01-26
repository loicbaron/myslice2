import React from 'react';

import { View, ViewHeader, ViewBody, Panel } from '../base/View';
import Title from '../base/Title';

import { ActivityList } from '../objects/Activity';
import RequestsList from '../RequestsList';

class ActivityView extends React.Component {

    constructor(props) {
        super(props);
    }

    render() {

        return (
            <View>
                <ViewHeader>
                    <Title title="Activity" />
                </ViewHeader>
                <ViewBody>
                    <Panel>
                        <ActivityList />
                    </Panel>
                    <Panel>
                        <RequestsList />
                    </Panel>
                </ViewBody>
            </View>
        );
    }
}

export default ActivityView;