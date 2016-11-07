import React from 'react';
import Select from 'react-select';

import List from '../base/List';
import LoadingPanel from '../LoadingPanel';
import Element from '../base/Element';
import ElementTitle from '../base/ElementTitle';
import ElementDetails from '../base/ElementDetails';
import LogList from '../base/LogList';
import DateTime from '../base/DateTime';

import store from '../../stores/ActivityStore';
import actions from '../../actions/ActivityActions';

class ActivityElement extends React.Component {

    constructor(props) {
        super(props);
    }

    label() {
        var object = this.props.activity.object.type.charAt(0) + this.props.activity.object.type.slice(1).toLowerCase();
        var dataType = '';
        if (this.props.activity.data.hasOwnProperty('type')) {
            dataType = this.props.activity.data.type.charAt(0) + this.props.activity.data.type.slice(1).toLowerCase();
        }

        switch(this.props.activity.action) {
            case 'CREATE':
                return 'New ' + object;
                break;
            case 'UPDATE':
                return 'Update ' + object;
                break;
            case 'DELETE':
                return 'Delete ' + object;
                break;
            case 'ADD':
                return 'Add ' + dataType + ' to ' + object;
                break;
            case 'REMOVE':
                return 'Remove ' + dataType + ' from ' + object;
                break;
        }
    }
    render() {
        var object = this.props.activity.object.type.toLowerCase();
        var status = this.props.activity.status.toLowerCase();

        if(Object.keys(this.props.activity.data).length === 0){
            var data = this.props.activity.object;
        }else{
            var data = this.props.activity.data;
        }
        return (
            <Element element={this.props.activity}
                     type={object}
                     status={status}
                     icon={object}
            >
                <ElementTitle label={this.label()} />
                <div className="row elementDate">
                    <div className="col-sm-3">
                        <span className="elementLabel">Created</span>
                        <br />
                        <DateTime timestamp={this.props.activity.created} />
                    </div>
                    <div className="col-sm-3">
                        <span className="elementLabel">Updated</span>
                        <br />
                        <DateTime timestamp={this.props.activity.updated} />
                    </div>
                </div>
                <ElementDetails data={data} key={this.props.activity.id} />
                <LogList log={this.props.activity.log} />
            </Element>
        );
    }
}

class ActivityFilter extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            'selected': []
        };
        this.setValue = this.setValue.bind(this);
    }

    componentDidMount() {
        // store
        // store.listen(this.onChange);

    }

    componentWillUnmount() {
        // store.unlisten(this.onChange);
    }


    setValue(value) {
		this.setState({ 'selected': value });
        this.props.handleChange(value);
	}

    getOptions() {
        return [
            { value: 'new', label: 'New', name: 'status' },
            { value: 'success', label: 'Success', name: 'status' },
            { value: 'pending', label: 'Pending', name: 'status' },
            { value: 'approved', label: 'Approved', name: 'status' },
            { value: 'denied', label: 'Denied', name: 'status' },
            { value: 'waiting', label: 'Waiting', name: 'status' },
            { value: 'running', label: 'Running', name: 'status' },
            { value: 'error', label: 'Error', name: 'status' },
            { value: 'warning', label: 'Warning', name: 'status' },

            { value: 'authority', label: 'Authority', name: 'object' },
            { value: 'user', label: 'User', name: 'object' },
            { value: 'project', label: 'Project', name: 'object' },
            { value: 'slice', label: 'Slice', name: 'object' },
            { value: 'resource', label: 'Resource', name: 'object' },

            { value: 'create', label: 'Create', name: 'action' },
            { value: 'update', label: 'Update', name: 'action' },
            { value: 'delete', label: 'Delete', name: 'action' },
            { value: 'add', label: 'Add', name: 'action' },
            { value: 'remove', label: 'Remove', name: 'action' },
        ];
    }

    renderLink() {
		return <a style={{ marginLeft: 5 }} href="/upgrade" target="_blank">C Upgrade here!</a>;
	}

	renderOption(option) {
		return (
            <span>
                <span className="selectShortname">{option.name}</span><br />
                <span className="selectLabel">{option.label}</span>
            </span>
        );
	}

	renderValue(option) {
		return (
            <span>
                <span className="selectShortname">{option.name}</span>&nbsp;
                <span className="selectLabel">{option.label}</span>
            </span>
        );

	}

    render() {
        let options = this.getOptions();

        return <Select
            name="form-field-name"
            multi={true}
            placeholder="Filter by..."
            value={this.state.selected}
            valueRenderer={this.renderValue}
            options={options}
            optionRenderer={this.renderOption}
            onChange={this.setValue}
            autoBlur={true}
        />
    }
}

ActivityFilter.propTypes = {
    handleChange: React.PropTypes.func,
    type: React.PropTypes.string
};

ActivityFilter.defaultProps = {
    type: "activity"
};

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
                                return <ActivityElement key={activity.id} activity={activity}/>;
                            })
                        }
                    </List>
                </div>
            );
        }


    }
}

export { ActivityElement, ActivityList };
