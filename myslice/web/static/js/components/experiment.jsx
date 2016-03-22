var ExperimentRow = React.createClass({

     render: function() {
         return (
             <div className="row">
                 <div className="col-md-6">
                     <div className="elementLabel">
                         {this.props.slice.name}
                     </div>
                     <div className="elementId">
                         {this.props.slice.id}
                     </div>
                     <div className="elementDate">
                        Created: { moment(this.props.slice.created).format("dddd, MMMM Do YYYY, H:mm") }
                        <br />
                        Updated: { moment(this.props.slice.updated).format("dddd, MMMM Do YYYY, H:mm") }
                     </div>
                 </div>
                 <div className="col-md-6">

                 </div>
             </div>
         );
     }
 });

var ExperimentList = React.createClass({

    getInitialState: function() {
        return experimentstore.getState();
    },

    componentDidMount: function() {
        // store
        experimentstore.listen(this.onChange);

        // action fetch slices
        experimentactions.fetchSlices();
    },

    componentWillUnmount() {
        experimentstore.unlisten(this.onChange);
    },

    onChange(state) {
        this.setState(state);
    },

    render: function() {
        if (this.state.errorMessage) {
            return (
                <div>Something is wrong</div>
            );
        }

        if (!this.state.slices.length) {
            return (
                <div>
                    Loading...
                </div>
            )
        }

        return (
            <div className="elementList">
            {this.state.slices.map(function(slice) { return <ExperimentRow key={slice.id} slice={slice}></ExperimentRow>; }) }
            </div>
        );
    }
});

ReactDOM.render(
        <ExperimentList />,
        document.getElementById('experiment-list')
);

var ExperimentAdd = React.createClass({

    render: function() {
        return (
            <button className="elementAdd"><img className="icon" src="/static/icons/plus.png" alt="+" /> New Experiment</button>
        );
    }
});

ReactDOM.render(
        <ExperimentAdd />,
        document.getElementById('slice-add')
);
