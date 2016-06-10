var React = require('react');
var store = require('../stores/ProjectsStore');
var actions = require('../actions/ProjectsActions');
var ProjectsRow = require('./ProjectsRow');
var TitlePanel = require('./TitlePanel');
var AddButton = require('./AddButton');

var ProjectsList = React.createClass({

    getInitialState: function() {
        return store.getState();
    },

    componentDidMount: function() {

        // listen on state changes
        store.listen(this.onChange);

        actions.fetchProjects();

    },

    componentWillUnmount() {
        store.unlisten(this.onChange);
    },

    onChange(state) {
        this.setState(state);
    },

    render: function() {
        var selected = this.state.selected;
        var projects = this.state.projects;

        if (this.state.errorMessage) {
            return (
                <div>Something is wrong</div>
            );
        }

        return (
            <ul className="elementList">
            { projects.map(function(project) {
                return <ProjectsRow key={project.id} project={project} selected={selected}></ProjectsRow>;
                })
            }
            </ul>
        );
    }
});

module.exports = React.createClass({

    addProject: function(){
        actions.selectProject(null);
    },

    render: function() {
        return (
            <div className="col-sm-6">

                <div className="p-header">
                    <div className="container-fluid">

                        <div className="row">
                            <div className="col-sm-12">

                                <div class="row">
                                    <div class="col-sm-6">

                                        <TitlePanel title="Projects" />

                                    </div>
                                    <div class="col-sm-6">

                                        <AddButton label="Add Project" handleClick={this.addProject}  />

                                    </div>
                                </div>


                            </div>
                        </div>


                    </div>
                </div>

                <div class="p-body">
                    <div class="container-fluid">
                        <div class="row">
                            <div class="col-md-12">
                                <ProjectsList />
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        );
    }
});