import React from 'react';

import LogRow from './LogRow';

const LogList = ({log}) =>
    <ul className="logList">
    {
         log.map(function(l) {
             return <LogRow key={l.timestamp} log={l} />;
         })
     }
    </ul>;

export default LogList;