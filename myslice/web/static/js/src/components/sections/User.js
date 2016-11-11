import React from 'react';

import { Section, SectionHeader, SectionBody, SectionTitle } from '../base/Section';
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

const UsersSectionSimple = ({users, title}) =>
    <Section>
        <SectionHeader>
            <SectionTitle title={title} />
        </SectionHeader>
        <SectionBody>
            <UserListSimple users={users} />
        </SectionBody>
    </Section>;

UsersSectionSimple.propTypes = {
    users: React.PropTypes.array.isRequired,
    title: React.PropTypes.string
};

UsersSectionSimple.defaultProps = {
    title: "Users"
};

export { UsersSection, UsersSectionSimple };