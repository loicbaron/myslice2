import React from 'react';

import { Section, SectionHeader, SectionBody, SectionTitle, SectionOptions } from '../base/Section';
import { UserList, UserListSimple } from '../objects/User';

const UsersSection = ({users, title}) =>
    <Section>
        <SectionHeader>
            <SectionTitle title={title} />
        </SectionHeader>
        <SectionBody>
            <UserList users={users} />
        </SectionBody>
    </Section>;

UsersSection.propTypes = {
    users: React.PropTypes.array.isRequired,
    title: React.PropTypes.string
};

UsersSection.defaultProps = {
    title: "Users"
};

const UsersSectionSimple = ({users, title, options}) =>
    <Section>
        <SectionHeader>
            <SectionTitle title={title} />
            <SectionOptions options={options} />
        </SectionHeader>
        <SectionBody>
            <UserListSimple users={users} />
        </SectionBody>
    </Section>;

UsersSectionSimple.propTypes = {
    users: React.PropTypes.array.isRequired,
    title: React.PropTypes.string,
    options: React.PropTypes.array
};

UsersSectionSimple.defaultProps = {
    title: "Users",
    options: []
};

export { UsersSection, UsersSectionSimple };