import React from 'react';

import { Section, SectionHeader, SectionBody, SectionTitle } from '../base/Section';
import { SliceList } from '../objects/Slice';

const SlicesSection = ({slices}) =>
    <Section>
        <SectionHeader>
            <SectionTitle title="Slices" />
        </SectionHeader>
        <SectionBody>
            <SliceList slices={slices} />
        </SectionBody>
    </Section>;

export { SlicesSection };