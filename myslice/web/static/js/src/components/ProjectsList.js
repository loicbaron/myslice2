import React from 'react';

import List from './base/List';
import ProjectsRow from'./ProjectsRow';

class ProjectsList extends React.Component {

    render() {

        if (!this.props.projects || this.props.projects.length==0) {
            return <List>No project</List>
        } else {
            return (
                <List detailed={ this.props.detailed}>
                {
                    this.props.projects.map(function(project) {
                        return <ProjectsRow key={project.id} project={project} detailed={ this.props.detailed} handleClick={this.props.handleClick} />;
                    }.bind(this))
                }
                </List>
            );
        }

    }
}

ProjectsList.propTypes = {
    projects: React.PropTypes.array.isRequired,
    handleClick: React.PropTypes.func,
    detailed: React.PropTypes.bool,
};

ProjectsList.defaultProps = {
};

export default ProjectsList;
