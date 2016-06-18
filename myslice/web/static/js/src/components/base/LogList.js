import React from 'react';

import LogRow from './LogRow';

class LogList extends React.Component {

    render() {
        return (
            <ul className="logList">
            {
                 this.props.log.map(function(log) {
                     return <LogRow key={log.timestamp} log={log} />;
                 })
             }
            </ul>
        );
    }
}

export default LogList;