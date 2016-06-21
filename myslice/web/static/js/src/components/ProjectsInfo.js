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
        var project = this.props.project;

        var filter = {
            type: 'project',
            id: project.id
        };

        return (
        <div>
            <ElementTitle label={this.props.project.shortname} />
            <ElementId id={this.props.project.id} />
            <p>
                <a href={project.url} target="_blank">{project.url}</a>
            </p>
            <p>
                {project.description}
            </p>
            <DateTime label="Start" timestamp={project.start_date} />
            <DateTime label="End" timestamp={project.end_date} />

            <Section>
                <SectionHeader>
                    <SectionTitle title="Users" />
                </SectionHeader>
                <SectionBody>
                    <UsersList belongTo={filter} />
                </SectionBody>
            </Section>
            
            <Section>
                <SectionHeader>
                    <SectionTitle title="Slices" />
                </SectionHeader>
                <SectionBody>
                    <SlicesList belongTo={filter} />
                </SectionBody>
            </Section>

        </div>
        );
    }
}


ProjectsInfo.propTypes = {
    project: React.PropTypes.object.isRequired
};

export default ProjectsInfo;
