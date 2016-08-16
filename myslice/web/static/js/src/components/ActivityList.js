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
        this.handleFilter = this.handleFilter.bind(this);
    }

    componentWillMount() {
        store.listen(this.onChange);
        actions.fetchActivity();
        actions.getUserToken();
    }

    componentDidMount() {
        actions.watchActivity()
    }

    componentWillUnmount() {
        store.unlisten(this.onChange);
    }

    onChange(state) {
        this.setState(state);
    }

    handleFilter(filter) {
        actions.fetchActivity(filter);

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
                
            let self = this;
            this.state.activity.sort(function(x, y) {
                return new Date(y.updated).getTime() - new Date(x.updated).getTime();
            })

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
