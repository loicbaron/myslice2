var ProjectLabel = React.createClass({

    label: function() {
        let label = '';
        switch(this.props.project.action) {
            case 'REQ':
                label = 'requested ' + this.props.project.object.type;
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
var ProjectStatus = React.createClass({
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

var ProjectRow = React.createClass({
     /*
     getInitialState () {
        return {
        'selected':false
        };
     },
     */
     handleClick(){
        projectactions.selectProject(this.props.project);
        /*
        if(this.state.selected){
            this.setState({'selected':false});
        }else{
            this.setState({'selected':true});
        }
        */
     },
     render: function() {
         if(this.props.selected == this.props.project.id){
            var liClass = 'elementBox selected';
         }else{
            var liClass = 'elementBox';
         }
         return (
             <li className={liClass} onClick={this.handleClick}>
                 <ProjectLabel project={this.props.project} />
                 <div className="row">
                     <div className="col-md-6">
                         <div className="elementId">
                             {this.props.project.id}
                         </div>
                         <div className="elementDate">
                            Created: { moment(this.props.project.created).format("DD/MM/YYYY H:mm") }
                            <br />
                            Updated: { moment(this.props.project.updated).format("DD/MM/YYYY H:mm") }
                         </div>
                     </div>
                     <div className="col-md-6">

                     </div>
                 </div>
                 <ProjectStatus status={this.props.project.status} />
             </li>
         );
     }
 });

var ProjectList = React.createClass({

    getInitialState: function() {
        return projectstore.getState();
    },

    componentDidMount: function() {
        

    // listen on state changes
    projectstore.listen(this.onChange);
    },

    componentWillUnmount() {
        projectstore.unlisten(this.onChange);
    },

    onChange(state) {
        this.setState(state);
    },

    render: function() {
        var selected = this.state.selected;
        var project = this.state.project;
        if (this.state.errorMessage) {
            return (
                <div>Something is wrong</div>
            );
        }

        return (
            <ul className="elementList">
            {project.map(function(project) { return <ProjectRow key={project.id} project={project} selected={selected}></ProjectRow>; }) }
            </ul>
        );
    }
});

ReactDOM.render(
        <ProjectList />,
        document.getElementById('projects-list')
);
/*
ReactDOM.render(
        <ProjectList type="REQUEST" />,
        document.getElementById('requests-list')
);
*/
