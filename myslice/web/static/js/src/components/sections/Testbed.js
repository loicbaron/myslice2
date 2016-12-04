import React from 'react';

import { TechnologyIcon } from '../base/Icon';
import { TestbedLabel } from '../objects/Testbed';

import { Section, SectionHeader, SectionBody, SectionTitle, SectionOptions } from '../base/Section';

const TestbedSectionPanel = ({testbeds, listOptions}) => {
    let technologies = [];

    testbeds.map(function(testbed) {
        if ((testbed.type == 'AM') && (testbed.technologies !== "undefined")) {
            technologies.push.apply(technologies, testbed.technologies);
        }
    });

    return <Section>
        <SectionBody>
            {
                technologies.map((technology) => {
                    return <div key={technology} className="col-sm-6 technologyBox">
                        <TechnologyIcon name={technology} />
                        {
                            testbeds.filter(function (testbed) {
                                if ((testbed.type == 'AM') && (testbed.technologies !== "undefined")) {
                                    return testbed.technologies.includes(technology);
                                }
                            }).map(function (testbed) {
                                return <TestbedLabel key={testbed.id} testbed={testbed} options={listOptions} />;
                            })
                        }
                    </div>
                })

            }
        </SectionBody>
    </Section>;
};

TestbedSectionPanel.propTypes = {
    testbeds: React.PropTypes.array.isRequired,
    listOptions: React.PropTypes.array
};

TestbedSectionPanel.defaultProps = {
    listOptions: []
};

export { TestbedSectionPanel }