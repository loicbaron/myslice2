import React from 'react';
import moment from 'moment';

const DateTime = (props) => {

    if (timestamp) {
        return (
            <div className="dateTime">
                <span className="elementLabel">{label}</span>
                {moment(timestamp).format("DD/MM/YYYY H:mm")}
            </div>
        );
    }

    return null;
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
                {moment(timestamp).calendar()}
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

const HumanDate = ({label, timestamp}) => {

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

HumanDate.propTypes = {
    timestamp: React.PropTypes.string,
    label: React.PropTypes.string
};

HumanDate.defaultProps = {
    timestamp : null,
    label: null
};

export { DateTime, CalendarDate, HumanDate };