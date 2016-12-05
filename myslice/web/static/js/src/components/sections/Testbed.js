import React from 'react';

import { TechnologyIcon } from '../base/Icon';
import { TestbedLabel } from '../objects/Testbed';

import { Section, SectionHeader, SectionBody, SectionTitle, SectionOptions } from '../base/Section';

const TestbedSectionPanel = ({testbeds, listOptions}) => {
    let technologies = [];
    let labels = [];
    // get the list of technologies defined for the testbeds
    testbeds.map(function(testbed) {
        if ((testbed.type == 'AM') && (testbed.technologies !== "undefined")) {
            technologies = technologies.concat(testbed.technologies);
        }
    });
    // there might be duplicates (low case first)
    technologies = technologies.map(t => t.toLowerCase()).filter((item, index, arr) => arr.indexOf(item) === index );

    technologies.forEach(function(t) {
        switch(t) {
            case 'iot':
                labels[t] = 'IoT';
                break;
            case 'vm':
                labels[t] = 'Virtual Machines';
                break;
            default:
                labels[t] = t.charAt(0).toUpperCase() + t.slice(1);
                break;
        }
    });

    return <Section>
        <SectionBody>
            <div className="row">
            {
                technologies.map((technology) => {
                    return <div key={"testbed-section-panel-" + technology} className="col-sm-10 col-sm-offset-1 technologyBox">
                        <div className="row">
                            <div className="col-sm-4 technologyLabel">
                                <img className={"technologyIcon " + technology} src={"/static/icons/technologies/" + technology + ".svg"} />
                                <br />
                                {labels[technology]}
                            </div>
                            <div className="col-sm-8 technologyTestbeds">
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
                        </div>
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