import React from 'react';

import List from './base/List';
import ProjectsRow from'./ProjectsRow';

class ProjectsList extends React.Component {

    render() {

        if (!this.props.projects) {
            return <List>No project found</List>
        } else {
            return (
                <List>
                {
                    this.props.projects.map(function(project) {
                        return <ProjectsRow key={project.id} project={project} setCurrent={this.props.setCurrent} current={this.props.current} />;
                    }.bind(this))
                }
                </List>
            );
        }

    }
}

ProjectsList.propTypes = {
    projects: React.PropTypes.array.isRequired,
    current: React.PropTypes.object,
    setCurrent: React.PropTypes.func
};

ProjectsList.defaultProps = {
    current: null,
    setCurrent: null
};

export default ProjectsList;