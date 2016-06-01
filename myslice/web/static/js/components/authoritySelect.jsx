var options = [
    { value: 'one', label: 'One' },
    { value: 'two', label: 'Two' }
];

function logChange(val) {
    console.log("Selected: " + val.value);
}
//
//const getOptions = (input) => {
//    console.log('==> get options');
//    store.dispatch(searchSlice(input));
//    return false;
//}


var AuthoritySelect = React.createClass({
    getInitialState () {
        return {};
    },

    setValue (value) {
		this.setState({ value });
		console.log('Support level selected:', value.label);
	},

    //getOptions: function(input) {
    //    console.log('getOptions ' + input);
    //},



    getProjects: function(input, callback) {
        axios.get('/api/v1/authorities').then((response) => {
            let s = response.data.result
            console.log(response)
            let options = [{
                label: 'Create new project',
                value: 'pro',
                disabled: true,
                link: this.renderLink()
            }]
            for(let i=0; i<10; i++) {
                options.push({
                    value: s[i].id,
                    label: s[i].name + "<br>" + s[i].id,
                })
            }

            callback(null, {
                options: options,
                complete: true
            });
        });

    },

    renderLink: function() {
		return <a style={{ marginLeft: 5 }} href="/upgrade" target="_blank">C Upgrade here!</a>;
	},
	renderOption: function(option) {
		return <span style={{ color: option.color }}>A{option.label} {option.link}</span>;
	},
	renderValue: function(option) {
		return <strong style={{ color: option.color }}>B{option.label}</strong>;
	},

    componentDidMount: function() {
        //this.props.options = []
        // store
        //experimentstore.listen(this.onChange);

        // action fetch slices
        //experimentactions.fetchSlices();
    },

    render: function () {
        return <Select.Async
            name="form-field-name"
            placeholder="Select your project"
            value={this.state.value}
            optionRenderer={this.renderOption}
            loadOptions={this.getProjects}
            valueRenderer={this.renderValue}
            onChange={this.setValue}
        />
    }
});


ReactDOM.render(
        <AuthoritySelect />,
        document.getElementById('authoritySelect')
);
