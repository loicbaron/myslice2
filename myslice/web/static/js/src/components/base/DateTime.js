import React from 'react';
import moment from 'moment';

const DateTime = (props) => {

        let datetime = null;
        let label = null;

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
    timestamp : null,
    label: null
};

const CalendarDate = ({label, timestamp}) => {

    if (timestamp) {
        return (
            <div className="dateTime">
                <span className="elementLabel">{label}</span>
                {moment(timestamp).fromNow()}
            </div>
        );
    }

    return null;

};

CalendarDate.propTypes = {
    timestamp: React.PropTypes.string,
    label: React.PropTypes.string
};

CalendarDate.defaultProps = {
    timestamp : null,
    label: null
};

export { DateTime, CalendarDate };