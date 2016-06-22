import React from 'react';
import moment from 'moment';

class DateTime extends React.Component {

    render() {
        var datetime = '';
        var label = '';

        if (this.props.label) {
            label = <div className="elementLabel">{this.props.label}</div>;
        }
        if (this.props.timestamp) {
            datetime = moment(this.props.timestamp).format("DD/MM/YYYY H:mm");
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

    }
}

DateTime.propTypes = {
    timestamp: React.PropTypes.string,
    label: React.PropTypes.string
};

DateTime.defaultProps = {
    timestamp : '',
    label: ''
};


export default DateTime;