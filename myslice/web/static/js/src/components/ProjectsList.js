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
                        return <ProjectsRow key={project.id} project={project} detailed={ this.props.detailed} setCurrent={this.props.setCurrent} current={this.props.current} />;
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
    setCurrent: React.PropTypes.func,
    detailed: React.PropTypes.bool,
};

ProjectsList.defaultProps = {
};

export default ProjectsList;
