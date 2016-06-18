import React from 'react';
import Select from 'react-select';

export default class ActivityFilter extends React.Component {

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