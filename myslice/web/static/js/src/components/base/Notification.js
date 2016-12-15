import React from 'react';
import { Icon } from './Icon';

class Notification extends React.Component {

    constructor(props) {
        super(props);
    }

    componentDidMount() {

    }

    render() {
        return <div className="notificationContainer">
            {this.props.children}
        </div>;
    }
}

const NotifyInfo = ({message}) =>
    <Notification>
        <div className="notificationInfo">
            <Icon name="info" /> {message}
        </div>
    </Notification>;

const NotifySuccess = ({message}) =>
    <Notification>
        <div className="notificationSuccess">
            <Icon name="success" /> {message}
        </div>
    </Notification>;

const NotifyError = ({message}) =>
    <Notification>
        <div className="notificationError">
            <Icon name="error" /> {message}
        </div>
    </Notification>;

const NotifyWarning = ({message}) =>
    <Notification>
        <div className="notificationWarning">
            <Icon name="warning" /> {message}
        </div>
    </Notification>;

export { NotifyInfo, NotifySuccess, NotifyError, NotifyWarning };


