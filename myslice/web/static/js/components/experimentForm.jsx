var options = [
    { value: 'one', label: 'One' },
    { value: 'two', label: 'Two' }
];

function logChange(val) {
    console.log("Selected: " + val);
}
//
//const getOptions = (input) => {
//    console.log('==> get options');
//    store.dispatch(searchSlice(input));
//    return false;
//}


var ProjectSelect = React.createClass({
    getInitialState () {
        return {
            text: ""
        };
    },



    //getOptions: function(input) {
    //    console.log('getOptions ' + input);
    //},

    getOptions: function(input, callback) {
        setTimeout(function () {
            //store.dispatch(searchSlice(input));
            callback(null, {
                options: [
                    {value: 'one', label: 'One'},
                    {value: 'two', label: 'Two'}
                ],
                // CAREFUL! Only set this to true when there are no more options,
                // or more specific queries will not be sent to the server.
                complete: true
            });
        }, 500);
    },

    componentDidMount: function() {
        // store
        //experimentstore.listen(this.onChange);

        // action fetch slices
        //experimentactions.fetchSlices();
    },

    render: function () {
        return <Select.Async
            name="form-field-name"
            value={this.state.text}
            loadOptions={this.getOptions}
            onChange={logChange}
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
        return <div>
            <input type="text" name="label" onChange={this.handleKeyPress} />
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
        return <div>
            <ProjectSelect />
            <ExperimentLabel />
        </div>
    }
});

ReactDOM.render(
        <ExperimentForm />,
        document.getElementById('experiment-form')
);
