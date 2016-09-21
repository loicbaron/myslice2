import React from 'react';

import List from '../base/List';
import TestbedsRow from'./Element';

const TestbedsList = ({testbeds, setCurrent, current}) =>
    <List>
    {
        testbeds.map(function(testbed) {
            return <TestbedsRow key={testbed.id} testbed={testbed} setCurrent={setCurrent} current={current} />;
        })
    }
    </List>;

TestbedsList.propTypes = {
    testbeds: React.PropTypes.array.isRequired,
    current: React.PropTypes.object,
    setCurrent: React.PropTypes.func
};

TestbedsList.defaultProps = {
    current: null,
    setCurrent: null,
};

export default TestbedsList;
