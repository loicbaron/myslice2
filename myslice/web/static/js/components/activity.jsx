var EventLabel = React.createClass({

    label: function() {
        let label = '';
        switch(this.props.event.action) {
            case 'REQ':
                label = 'requested ' + this.props.event.object.type;
        }
        return label;
    },

    render: function () {
        return (

            <div className="row">
                <div className="col-md-12">
                    <div className="elementIcon">
                <img src="/static/icons/projects-w-24.png" alt="" />
            </div>
                    <div className="elementLabel">{ this.label() }</div>
                </div>
            </div>
        )
    }
});
var EventStatus = React.createClass({
    render: function () {
        return (
            <div className="row">
                <div className="col-md-12">
                    <div className="elementStatus">{ this.props.status }</div>
                </div>
            </div>
        )
    }
});

var EventRow = React.createClass({

     render: function() {
         return (
             <li className="elementBox">
                 <EventLabel event={this.props.event} />
                 <div className="row">
                     <div className="col-md-6">
                         <div className="elementId">
                             {this.props.event.id}
                         </div>
                         <div className="elementDate">
                            Created: { moment(this.props.event.created).format("DD/MM/YYYY H:mm") }
                            <br />
                            Updated: { moment(this.props.event.updated).format("DD/MM/YYYY H:mm") }
                         </div>
                     </div>
                     <div className="col-md-6">

                     </div>
                 </div>
                 <EventStatus status={this.props.event.status} />
             </li>
         );
     }
 });

var EventList = React.createClass({

    getInitialState: function() {
        return activitystore.getState();
    },

    componentDidMount: function() {
        // listen on state changes
        activitystore.listen(this.onChange);

        // setup activity
        activityactions.setupActivity();

        // action fetch slices
        //activitystore.fetchSlices();
    },

    componentWillUnmount() {
        activitystore.unlisten(this.onChange);
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

        if (!this.state.events.length) {
            return (
                <div>
                    Loading...
                </div>
            )
        }

        return (
            <ul className="elementList">
            {this.state.events.map(function(event) { return <EventRow key={event.id} event={event}></EventRow>; }) }
            </ul>
        );
    }
});

ReactDOM.render(
        <EventList />,
        document.getElementById('activity-list')
);