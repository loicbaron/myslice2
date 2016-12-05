import React from 'react';

import { List, ListSimple } from '../base/List';
import { Element } from '../base/Element';
import ElementTitle from '../base/ElementTitle';
import ElementId from '../base/ElementId';
import DateTime from '../base/DateTime';
import { Icon } from '../base/Icon';

const TestbedElement = ({testbed, isSelected, handleSelect, options}) => {
    let status = testbed.status.online ? 'online' : 'offline';
    let icon = testbed.type == 'AM' ? 'testbed' : 'registry';

    return (
        <Element element={testbed}
                 type="testbed"
                 handleSelect={handleSelect}
                 status={status}
                 icon={icon}
        >
            <ElementTitle label={testbed.name} detail={testbed.hostname}/>
            <ElementId id={testbed.id}/>

            <div className="elementDetail">
                <span className="elementLabel">API</span>
                &nbsp;{testbed.api.protocol}
                &nbsp;{testbed.api.type}
                &nbsp;&nbsp;
                <span className="elementLabel">version</span> {testbed.api.version}
                <br />
                <span className="elementLabel">URL</span> {testbed.url}
            </div>
            <div className="row elementDate">
                <div className="col-sm-3">
                    <span className="elementLabel">Last update</span>
                    <br />
                    <DateTime timestamp={null}/>
                </div>
            </div>
        </Element>
    );
};


TestbedElement.propTypes = {
    testbed: React.PropTypes.object.isRequired,
};

TestbedElement.defaultProps = {
};

const TestbedList = ({testbeds, selected, handleSelect}) => {

    return <List>
        {
            testbeds.map(function (testbed) {
                let isSelected = selected.some(function (el) {
                    return el.id === testbed.id;
                });

                return <TestbedElement key={testbed.id}
                                       testbed={testbed}
                                       isSelected={isSelected}
                                       handleSelect={handleSelect} />;
            })
        }
    </List>;
};

TestbedList.propTypes = {
    testbeds: React.PropTypes.array.isRequired,
    handleSelect: React.PropTypes.func,
    selected: React.PropTypes.array || React.Proptypes.object
};

TestbedList.defaultProps = {
    selected: [],
};

const TestbedLabel = ({testbed, options}) => {
    let status = testbed.connection.online ? 'online' : 'offline';

    return (<div className="labelBox">
                <ElementTitle label={testbed.name} />
                <ul className="labelOptions">
                    <li key={"status-" + testbed.id} className={"labelStatus " + status}>
                        <Icon name={status} />{status}
                    </li>
                {
                    options.map(function(option) {
                        if ((typeof option.label !== "undefined") && (typeof option.callback !== "undefined")) {
                            return <li key={option.icon + "-" + testbed.id} className={ "labelOption visible " + option.icon }
                                        onClick={() => option.callback(testbed) }>
                                <Icon name={option.icon} />{option.label}
                            </li>;
                        }
                    })
                }
                </ul>
            </div>
    );
};


TestbedLabel.propTypes = {
    testbed: React.PropTypes.object.isRequired,
};

TestbedLabel.defaultProps = {
    options: []
};

export { TestbedElement, TestbedList, TestbedLabel };
