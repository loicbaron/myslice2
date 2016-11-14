import React from 'react';
import Select from 'react-select';

import store from '../../stores/forms/SelectAuthority';
import actions from '../../actions/forms/SelectAuthority';

class SelectAuthority extends React.Component {

    constructor(props) {
        super(props);
        this.state = store.getState();
        this.onChange = this.onChange.bind(this);
        this.setValue = this.setValue.bind(this);
    }

    componentDidMount() {
        // store
        store.listen(this.onChange);

        // action fetch authorities
        // defer() allows to be called during render of another component
        actions.fetchAuthorities.defer();
    }

    componentWillUnmount() {
        store.unlisten(this.onChange);
    }

    onChange(state) {
        this.setState(state);
    }

    setValue(value) {
		this.setState({ value });
        if (value) {
            this.props.handleChange(value.value);
        } else {
            this.props.handleChange(null);
        }
	}

    getOptions() {
        return this.state.authorities.map(function(authority) {
            return {
                value: authority.id,
                label: authority.name,
                shortname: authority.shortname
            }
        });
    }

    renderLink() {
		return <a style={{ marginLeft: 5 }} href="/upgrade" target="_blank">C Upgrade here!</a>;
	}

	renderOption(option) {
		return (
            <span>
                <span className="selectLabel">{option.label}</span>
                &nbsp;
                <span className="selectShortname">({option.shortname})</span>
            </span>
        );
	}

	renderValue(option) {
		return (
            <span>
                <span>{option.label}</span>
                &nbsp;
                <i>{option.shortname}</i>
            </span>
        );

	}

    render() {
        var placeholder = this.props.placeholder || "Select Organization";
        var options = this.getOptions();

        if (this.props.selected) {
            this.state.value = this.props.selected;
        }

        return <Select
                    name="authority"
                    placeholder={placeholder}
                    value={this.state.value}
                    valueRenderer={this.renderValue}
                    options={options}
                    optionRenderer={this.renderOption}
                    onChange={this.setValue}
                />
    }
}

export default SelectAuthority;