import React from 'react';

import LogRow from './LogRow';

/*class LogList extends React.Component {

    render() {
        
        this.props.log.sort(function(x, y) {
                return new Date(y.timestamp).getTime() - new Date(x.timestamp).getTime();
        })

        return (
            <ul className="logList">
            {
                 this.props.log.map(function(log) {
                     return <LogRow  key={log.timestamp + log.type} log={log} />;
                 })
             }
            </ul>
        );
    }
}*/


const LogList = ({log}) =>

    <ul className="logList">
    {
         log.map(function(l) {
             return <LogRow key={l.timestamp} log={l} />;
         })
     }
    </ul>;


export default LogList;