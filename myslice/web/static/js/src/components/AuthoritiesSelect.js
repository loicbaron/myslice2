/*
 * Authority Select component
 * requires: authorities actions and store
 */
var React = require('react');
var Select = require('react-select');
var store = require('../stores/AuthoritiesStore');
var actions = require('../actions/AuthoritiesActions');

module.exports = React.createClass({

    getInitialState () {
        return store.getState();
    },

    componentDidMount: function() {
        // store
        store.listen(this.onChange);

        // action fetch authorities
        actions.fetchAuthorities();

    },

    componentWillUnmount() {
        store.unlisten(this.onChange);
    },

    onChange(state) {
        this.setState(state);
    },

    setValue(value) {
		this.setState({ value });
        this.props.handleChange(value.value);
	},

    getOptions: function() {
        return this.state.authorities.map(function(authority) {
            return {
                value: authority.id,
                label: authority.name,
                shortname: authority.shortname
            }
        });
    },

    renderLink: function() {
		return <a style={{ marginLeft: 5 }} href="/upgrade" target="_blank">C Upgrade here!</a>;
	},

	renderOption: function(option) {
		return (
            <span>
                <span>{option.label}</span>
                &nbsp;
                <i>{option.shortname}</i>
            </span>
        );
	},

	renderValue: function(option) {
		return (
            <span>
                <span>{option.label}</span>
                &nbsp;
                <i>{option.shortname}</i>
            </span>
        );

	},

    render: function () {
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
});