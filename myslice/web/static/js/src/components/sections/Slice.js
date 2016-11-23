import React from 'react';

import { Section, SectionHeader, SectionBody, SectionTitle, SectionOptions } from '../base/Section';
import { SliceList } from '../objects/Slice';

const SlicesSection = ({slices, title, sectionOptions, listOptions}) =>
    <Section>
        <SectionHeader>
            <SectionTitle title="Slices" />
            <SectionOptions options={sectionOptions} />
        </SectionHeader>
        <SectionBody>
            <SliceList slices={slices} options={listOptions} />
        </SectionBody>
    </Section>;

SlicesSection.propTypes = {
    slices: React.PropTypes.array.isRequired,
    title: React.PropTypes.string,
    sectionOptions: React.PropTypes.array,
    listOptions: React.PropTypes.array
};

SlicesSection.defaultProps = {
    title: "Slices",
    sectionOptions: [],
    listOptions: []
};

export { SlicesSection };