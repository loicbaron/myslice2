import React from 'react';
import Select from 'react-select';
import store from '../stores/AuthoritiesStore';
import actions from '../actions/AuthoritiesActions';

export default class AuthoritiesSelect extends React.Component {

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
        actions.fetchAuthorities();

    }

    componentWillUnmount() {
        store.unlisten(this.onChange);
    }

    onChange(state) {
        this.setState(state);
    }

    setValue(value) {
		this.setState({ value });
        this.props.handleChange(value.value);
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
                <span>{option.label}</span>
                &nbsp;
                <i>{option.shortname}</i>
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
        let options = this.getOptions();

        return <Select
            name="form-field-name"
            placeholder="Select your Authority"
            value={this.state.value}
            valueRenderer={this.renderValue}
            options={options}
            optionRenderer={this.renderOption}
            onChange={this.setValue}
        />
    }
}