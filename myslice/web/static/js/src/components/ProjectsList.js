import React from 'react';

import store from '../stores/ProjectsStore';
import actions from '../actions/ProjectsActions';

import List from './base/List';
import ProjectsRow from'./ProjectsRow';

class ProjectsList extends React.Component {

    constructor(props) {
        super(props);
        this.state = store.getState();
        this.onChange = this.onChange.bind(this);
    }

    componentDidMount() {
        store.listen(this.onChange);

        actions.fetchProjects({
                belongTo: this.props.belongTo
        });


    }

    componentWillUnmount() {
        store.unlisten(this.onChange);
    }

    onChange(state) {
        this.setState(state);
    }

    render() {
        return (
            <List>
            {
                this.state.projects.map(function(project) {
                    return <ProjectsRow key={project.id} project={project} select={this.props.select} />;
                }.bind(this))
            }
            </List>
        );
    }
}

ProjectsList.propTypes = {
    belongTo: React.PropTypes.object,
    select: React.PropTypes.bool
};

ProjectsList.defaultProps = {
    belongTo: { type: null, id: null},
    select: false
};

export default ProjectsList;