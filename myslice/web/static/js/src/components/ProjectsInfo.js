import React from 'react';

import ElementId from './base/ElementId';
import Section from './base/Section';
import SectionHeader from './base/SectionHeader';
import SectionBody from './base/SectionBody';
import SectionTitle from './base/SectionTitle';
import DateTime from './base/DateTime';

import { UserList } from './objects/User';
import { SliceList } from './objects/Slice';

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
                            <UserList users={this.props.element.users} removeUser={true} />
                        </SectionBody>
                    </Section>
        }

        if (this.props.element.slices.length > 0) {
            slices = <Section>
                        <SectionHeader>
                            <SectionTitle title="Slices" />
                        </SectionHeader>
                        <SectionBody>
                            <SliceList slices={this.props.element.slices} removeSlice={true} />
                        </SectionBody>
                    </Section>
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
