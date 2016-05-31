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
        axios.get('/api/v1/slices').then((response) => {
            let s = response.data.slices
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

var ExperimentLabel = React.createClass({
    getInitialState() {
        return {
            label: "",
            name: "test"
        };
    },

    handleKeyPress(event) {
        this.setState(
            {
                label: event.target.value,
                name: this.normaliseLabel(event.target.value)
            }
        );
    },

    normaliseLabel(text) {
        return text.replace(/[^a-z0-9]+/gi, '').replace(/^-*|-*$/g, '').toLowerCase();
    },

    render: function () {
        return <div className="form-group">
            <label htmlFor="sliceName">Slice name</label>
            <input id="sliceName" className="form-control" type="text" name="label" onChange={this.handleKeyPress} placeholder="Slice name" />
            <div>{this.state.name}</div>
        </div>
    }
});


var ExperimentForm = React.createClass({
    getInitialState () {
        return {
            text: ""
        };
    },

    render: function () {
        return <form>
            <ProjectSelect />
            <ExperimentLabel />
            <button type="submit" className="btn btn-default">Submit</button>
        </form>
    }
});

ReactDOM.render(
        <AuthoritySelect />,
        document.getElementById('experiment-form')
);
