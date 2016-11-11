import React from 'react';

import { Section, SectionHeader, SectionBody, SectionTitle } from '../base/Section';
import { UserList } from '../objects/User';

const SectionUserList = ({users}) =>
    <Section>
        <SectionHeader>
            <SectionTitle title="Users" />
        </SectionHeader>
        <SectionBody>
            <UserList users={users} />
        </SectionBody>
    </Section>;

export { SectionUserList };