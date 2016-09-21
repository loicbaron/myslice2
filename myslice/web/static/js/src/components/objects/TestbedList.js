import React from 'react';

import List from '../base/List';
import TestbedElement from'./TestbedElement';

const TestbedList = ({testbeds, setCurrent, current}) =>
    <List>
    {
        testbeds.map(function(testbed) {
            return <TestbedElement key={testbed.id} testbed={testbed} setCurrent={setCurrent} current={current} />;
        })
    }
    </List>;

TestbedList.propTypes = {
    testbeds: React.PropTypes.array.isRequired,
    current: React.PropTypes.object,
    setCurrent: React.PropTypes.func
};

TestbedList.defaultProps = {
    current: null,
    setCurrent: null,
};

export default TestbedList;
