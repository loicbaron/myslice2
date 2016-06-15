import React from 'react';
import moment from 'moment';

class Log extends React.Component {

    render() {

        return (
            <div className="row">
                <div className="col-md-12 logLine">
                    <i className="fa fa-warning logIcon"></i>
                    <span className="logTimestamp">{ moment(this.props.log.timestamp).format("DD/MM/YYYY H:mm") }</span>
                    <span className="logType">{ this.props.log.type }</span>
                    <span className="logMessage">{ this.props.log.message }</span>
                </div>
            </div>
        );
    }
}

export default Log;