import React from 'react';

import List from './base/List';
import ProjectsRow from'./ProjectsRow';

class ProjectsList extends React.Component {
    
    render() {
        return (
            <List>
            {
                this.props.projects.map(function(project) {
                    return <ProjectsRow key={project.id} project={project} selected={this.props.selected} selectProject={this.props.selectProject} />;
                }.bind(this))
            }
            </List>
        );
    }
}

ProjectsList.defaultProps = {
    'filter' : {
        'type' : null,
        'value' : null
    }

};

export default ProjectsList;