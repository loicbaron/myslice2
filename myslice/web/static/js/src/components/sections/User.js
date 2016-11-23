import React from 'react';

import { Section, SectionHeader, SectionBody, SectionTitle, SectionOptions } from '../base/Section';
import { UserList, UserListSimple } from '../objects/User';

const UsersSection = ({users, title, sectionOptions, listOptions}) =>
    <Section>
        <SectionHeader>
            <SectionTitle title={title} />
            <SectionOptions options={sectionOptions} />
        </SectionHeader>
        <SectionBody>
            <UserList users={users} options={listOptions} />
        </SectionBody>
    </Section>;

UsersSection.propTypes = {
    users: React.PropTypes.array.isRequired,
    title: React.PropTypes.string,
    sectionOptions: React.PropTypes.array,
    listOptions: React.PropTypes.array
};

UsersSection.defaultProps = {
    title: "Users",
    sectionOptions: [],
    listOptions: []
};

const UsersSectionSimple = ({users, title, sectionOptions, listOptions}) =>
    <Section>
        <SectionHeader>
            <SectionTitle title={title} />
            <SectionOptions options={sectionOptions} />
        </SectionHeader>
        <SectionBody>
            <UserListSimple users={users} options={listOptions} />
        </SectionBody>
    </Section>;

UsersSectionSimple.propTypes = {
    users: React.PropTypes.array.isRequired,
    title: React.PropTypes.string,
    sectionOptions: React.PropTypes.array,
    listOptions: React.PropTypes.array
};

UsersSectionSimple.defaultProps = {
    title: "Users",
    sectionOptions: [],
    listOptions: []
};

export { UsersSection, UsersSectionSimple };