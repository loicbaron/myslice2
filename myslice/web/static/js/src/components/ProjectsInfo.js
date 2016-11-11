import React from 'react';

import ElementId from './base/ElementId';
import { SectionUserList } from './sections/User';
import { SectionSliceList } from './sections/Slice';
import DateTime from './base/DateTime';


class ProjectsInfo extends React.Component {

    render() {
        var project = this.props.element.project;
        var users = null;
        var slices = null;

        if (this.props.element.users.length > 0) {
            users = <SectionUserList users={this.props.element.users} removeUser={true} />;

        }

        if (this.props.element.slices.length > 0) {
            slices = <SectionSliceList slices={this.props.element.slices} removeSlice={true} />;
        }

        return (
            <div>
                <ElementId id={project.id} />
                <p>
                    <a href={project.url} target="_blank">{project.url}</a>
                </p>
                <p>
                    {project.description}
                </p>
                <DateTime label="Start" timestamp={project.start_date} />
                <DateTime label="End" timestamp={project.end_date} />
                {slices}
                {users}
            </div>
        );
    }
}


ProjectsInfo.propTypes = {
    element: React.PropTypes.object.isRequired
};

export default ProjectsInfo;
