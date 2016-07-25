import React from 'react';
import DateTime from './DateTime';

const LogRow = (log) =>
    <li className="logRow">
        <i className="fa fa-warning logIcon"></i>
        <span className="logTimestamp"><DateTime timestamp={log.timestamp} /></span>
        <span className="logType">{log.type}</span>
        <span className="logMessage">{log.message}</span>
    </li>;

export default LogRow;