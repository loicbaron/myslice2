import React from 'react';
import DateTime from './DateTime';

class LogRow extends React.Component {

    render() {

        return (
            <li className="logRow">
                <i className="fa fa-warning logIcon"></i>
                <span className="logTimestamp"><DateTime timestamp={this.props.log.timestamp} /></span>
                <span className="logType">{ this.props.log.type }</span>
                <span className="logMessage">{ this.props.log.message }</span>
            </li>
        );
    }
}

export default LogRow;