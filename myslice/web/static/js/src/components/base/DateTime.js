import React from 'react';
import moment from 'moment';

const DateTime = (props) => {

        var datetime = '';
        var label = '';

        if (props.label) {
            label = <div className="elementLabel">{props.label}</div>;
        }
        if (props.timestamp) {
            datetime = moment(props.timestamp).format("DD/MM/YYYY H:mm");
        }

        if (datetime) {
            return (
                <div className="dateTime">
                    {label}
                    {datetime}
                </div>
            );
        } else {
            return null;
        }
};

DateTime.propTypes = {
    timestamp: React.PropTypes.string,
    label: React.PropTypes.string
};

DateTime.defaultProps = {
    timestamp : '',
    label: ''
};

export default DateTime;