import React from 'react';

import { List, ListSimple } from '../base/List';
import { Element } from '../base/Element';
import ElementTitle from '../base/ElementTitle';
import ElementId from '../base/ElementId';
import DateTime from '../base/DateTime';

const TestbedElement = ({testbed, isSelected, handleSelect}) => {
    testbed.status=testbed.status.online ? 'online' : 'offline';
    return (
     <Element element={testbed}
              type="testbed"
              handleSelect={handleSelect}
              status={testbed.status}
              icon={testbed.type == 'AM' ? 'testbed' : 'registry'}
     >
         <ElementTitle label={testbed.name} detail={testbed.hostname} />
         <ElementId id={testbed.id} />

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
                 <DateTime timestamp={null} />
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

    if (!Array.isArray(selected)) {

    }

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
}
TestbedList.propTypes = {
    testbeds: React.PropTypes.array.isRequired,
    handleSelect: React.PropTypes.func,
    selected: React.PropTypes.array || React.Proptypes.object
};

TestbedList.defaultProps = {
    selected: [],
};


export { TestbedElement, TestbedList };
