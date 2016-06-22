import React from 'react';

import ElementTitle from './base/ElementTitle';
import ElementId from './base/ElementId';
import Section from './base/Section';
import SectionHeader from './base/SectionHeader';
import SectionBody from './base/SectionBody';
import SectionTitle from './base/SectionTitle';
import DateTime from './base/DateTime';

import UsersList from './UsersList';
import SlicesList from './SlicesList';

class ProjectsInfo extends React.Component {

    render() {
        var project = this.props.element.project;
        var users = null;
        var slices = null;

        if (this.props.element.users.length > 0) {
            users = <Section>
                        <SectionHeader>
                            <SectionTitle title="Users" />
                        </SectionHeader>
                        <SectionBody>
                            <UsersList users={this.props.element.users} />
                        </SectionBody>
                    </Section>
        }

        if (this.props.element.slices.length > 0) {
            slices = <Section>
                        <SectionHeader>
                            <SectionTitle title="Slices" />
                        </SectionHeader>
                        <SectionBody>
                            <SlicesList slices={this.props.element.slices} />
                        </SectionBody>
                    </Section>
        }

        return (
        <div>
            <ElementTitle label={project.shortname} />
            <ElementId id={project.id} />
            <p>
                <a href={project.url} target="_blank">{project.url}</a>
            </p>
            <p>
                {project.description}
            </p>
            <DateTime label="Start" timestamp={project.start_date} />
            <DateTime label="End" timestamp={project.end_date} />

            {users}
            
            {slices}

        </div>
        );
    }
}


ProjectsInfo.propTypes = {
    element: React.PropTypes.object.isRequired
};

export default ProjectsInfo;
