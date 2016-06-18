import React from 'react';
import store from '../stores/ActivityStore';
import actions from '../actions/ActivityActions';

import List from './base/List';
import LoadingPanel from './LoadingPanel';

import ActivityFilter from './ActivityFilter';
import ActivityRow from'./ActivityRow';

class ActivityList extends React.Component {

    constructor(props) {
        super(props);
        this.state = store.getState();
        this.onChange = this.onChange.bind(this);
    }

    componentDidMount() {
        store.listen(this.onChange);
        actions.fetchActivity();
        //actions.watchActivity();
    }

    componentWillUnmount() {
        store.unlisten(this.onChange);
    }

    onChange(state) {
        this.setState(state);
    }

    handleFilter(value) {
        console.log(value);
        actions.fetchActivity(value);
    }

    render() {

        if (this.state.errorMessage) {
            return (
                <div>Something is wrong</div>
            );
        }

        if (!this.state.activity) {
            return <LoadingPanel show="true" />;
        } else {
            return (
                <div>
                    <ActivityFilter handleChange={this.handleFilter} />
                    <List>
                        {
                            this.state.activity.map(function (activity) {
                                return <ActivityRow key={activity.id} activity={activity}/>;
                            })
                        }
                    </List>
                </div>
            );
        }
    }
}

export default ActivityList;