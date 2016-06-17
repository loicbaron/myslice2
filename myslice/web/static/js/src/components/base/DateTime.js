import React from 'react';
import moment from 'moment';

class DateTime extends React.Component {

    render() {

        return (
            <span className="dateTime">
                { moment(this.props.timestamp).format("DD/MM/YYYY H:mm") }
            </span>
        );

    }
}

export default DateTime;