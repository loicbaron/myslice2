import React from 'react';

import { TechnologyIcon } from '../base/Icon';
import { TestbedLabel } from '../objects/Testbed';

import { Section, SectionHeader, SectionBody, SectionTitle, SectionOptions } from '../base/Section';

const TestbedSectionPanel = ({testbeds, listOptions}) => {
    let technologies = [];
    // get the list of technologies defined for the testbeds
    testbeds.map(function(testbed) {
        if ((testbed.type == 'AM') && (testbed.technologies !== "undefined")) {
            technologies = technologies.concat(testbed.technologies);
        }
    });
    // there might be duplicates
    technologies = technologies.filter((item, index, arr) => arr.indexOf(item) === index );

    return <Section>
        <SectionBody>
            <div className="row">
            {
                technologies.map((technology) => {
                    return <div key={"testbed-section-panel-" + technology} className="col-sm-6 technologyBox">
                        <TechnologyIcon name={technology} />
                        {
                            testbeds.filter(function (testbed) {
                                if ((testbed.type == 'AM') && (testbed.technologies !== "undefined")) {
                                    return testbed.technologies.includes(technology);
                                }
                            }).map(function (testbed) {
                                return <TestbedLabel key={"testbed-label-" + testbed.id} testbed={testbed} options={listOptions} />;
                            })
                        }
                    </div>
                })

            }
            </div>
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