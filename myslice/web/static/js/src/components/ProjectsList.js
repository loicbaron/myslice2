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
        actions.fetchProjects();
    }

    componentWillUnmount() {
        store.unlisten(this.onChange);
    }

    onChange(state) {
        this.setState(state);
    }
    
    render() {
        let projects = this.state.projects;

        if (this.state.errorMessage) {
            return (
                <div>Something is wrong</div>
            );
        }

        return (
            <List>
            {
                projects.map(function(project) {
                    return <ProjectsRow key={project.id} project={project}></ProjectsRow>;
                })
            }
            </List>
        );
    }
}

export default ProjectsList;