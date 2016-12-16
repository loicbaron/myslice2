import React from 'react';

import { Section, SectionHeader, SectionBody, SectionTitle, SectionOptions } from '../base/Section';
import { ResourceList } from '../objects/Resource';

const ResourcesSection = ({resources, title, sectionOptions, listOptions}) =>
    <Section>
        <SectionHeader>
            <SectionTitle title="Resources" />
            <SectionOptions options={sectionOptions} />
        </SectionHeader>
        <SectionBody>
            <ResourceList resources={resources} options={listOptions} />
        </SectionBody>
    </Section>;

ResourcesSection.propTypes = {
    resources: React.PropTypes.array.isRequired,
    title: React.PropTypes.string,
    sectionOptions: React.PropTypes.array,
    listOptions: React.PropTypes.array
};

ResourcesSection.defaultProps = {
    title: "Resources",
    sectionOptions: [],
    listOptions: []
};

export { ResourcesSection };
