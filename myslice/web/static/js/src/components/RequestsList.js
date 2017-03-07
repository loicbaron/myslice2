import React from 'react';

import store from '../stores/RequestsStore';
import actions from '../actions/RequestsActions';
import { List, ListSimple } from './base/List';
import LoadingPanel from './LoadingPanel';

import RequestsFilter from './RequestsFilter';
import RequestsRow from './RequestsRow';

class RequestsList extends React.Component {

    constructor(props) {
        super(props);
        this.state = store.getState();
        this.onChange = this.onChange.bind(this);
        this.handleFilter = this.handleFilter.bind(this);
        this.executeAction = this.executeAction.bind(this);
    }

    componentWillMount() {
        store.listen(this.onChange);
        if(this.props.filters){
            actions.fetchRequests(this.props.filters);
        }else{
            actions.fetchRequests();
        }
    }

    componentDidMount() {
    }
    
    componentWillUnmount() {
        store.unlisten(this.onChange);
    }

    onChange(state) {
        this.setState(state);
    }

    handleFilter(filter) {
        actions.fetchRequests(filter);
    }

    executeAction(data) {
        actions.executeAction(data); 
    }

    render() {

        if (this.state.errorMessage) {
            return (
                <div>Something is wrong</div>
            );
        }
        
        if (!this.state.requests) {
            
            return <LoadingPanel show="true" />;
        
        } else { 
            // closure
            let self = this;
            this.state.requests.sort(function(x, y) {
                return new Date(y.updated).getTime() - new Date(x.updated).getTime();
            })
            if(this.props.displayFilters){
                var filter = <RequestsFilter handleChange={this.handleFilter} />
            }else{
                var filter = "";
            }
            return (
                <div>
                    {filter}
                    <List>
                        {
                            this.state.requests.map(function (request) {
                                return <RequestsRow key={request.id} 
                                                    request={request} 
                                                    executeAction={self.executeAction}
                                                    />;
                            })
                        }
                    </List>
                </div>
            );
        }
        
    }
}

RequestsList.propTypes = {
    type: React.PropTypes.string,
    filters: React.PropTypes.array,
    displayFilters: React.PropTypes.bool
}

RequestsList.defaultProps = {
    type: "requests",
    filters: [],
    displayFilters: true
}

export default RequestsList;
