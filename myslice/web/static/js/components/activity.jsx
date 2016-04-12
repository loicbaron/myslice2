var ActivityLabel = React.createClass({

    label: function() {
        let label = '';
        switch(this.props.activity.action) {
            case 'REQ':
                label = 'requested ' + this.props.activity.object.type;
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
var ActivityStatus = React.createClass({
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

var ActivityRow = React.createClass({

     render: function() {
         return (
             <li className="elementBox">
                 <ActivityLabel activity={this.props.activity} />
                 <div className="row">
                     <div className="col-md-6">
                         <div className="elementId">
                             {this.props.activity.id}
                         </div>
                         <div className="elementDate">
                            Created: { moment(this.props.activity.created).format("DD/MM/YYYY H:mm") }
                            <br />
                            Updated: { moment(this.props.activity.updated).format("DD/MM/YYYY H:mm") }
                         </div>
                     </div>
                     <div className="col-md-6">

                     </div>
                 </div>
                 <ActivityStatus status={this.props.activity.status} />
             </li>
         );
     }
 });

var ActivityList = React.createClass({

    getInitialState: function() {
        return activitystore.getState();
    },

    componentDidMount: function() {
        

        // listen on state changes
        activitystore.listen(this.onChange);
    },

    componentWillUnmount() {
        activitystore.unlisten(this.onChange);
    },

    onChange(state) {
        this.setState(state);
    },

    getActivity() {
        return this.state.activity.filter(function(activity) { return activity.type == this.props.type }.bind(this));
    },

    render: function() {

        let activity = this.getActivity();
        console.log(activity);
        if (this.state.errorMessage) {
            return (
                <div>Something is wrong</div>
            );
        }

        // if (!activity.length) {
        //     return (
        //         <div>
        //             Loading...
        //         </div>
        //     )
        // }

        return (
            <ul className="elementList">
            {activity.map(function(activity) { return <ActivityRow key={activity.id} activity={activity}></ActivityRow>; }) }
            </ul>
        );
    }
});

ReactDOM.render(
        <ActivityList type="EVENT" />,
        document.getElementById('events-list')
);

ReactDOM.render(
        <ActivityList type="REQUEST" />,
        document.getElementById('requests-list')
);