import React from 'react';

import { NotifyInfo, NotifySuccess, NotifyError, NotifyWarning  } from './Notification';

const View = ({children, notification}) => {

    let notificationElement = null;

    if (notification) {
        switch(notification.type) {
            case 'info':
                notificationElement = <NotifyInfo message={notification.message} />;
                break;
            case 'success':
                notificationElement = <NotifySuccess message={notification.message} />;
                break;
            case 'error':
                notificationElement = <NotifyError message={notification.message} />;
                break;
            case 'warning':
                notificationElement = <NotifyWarning message={notification.message} />;
                break;
        }

    }

    return (
        <div className="view">
            {children}
            {notificationElement}
        </div>
    );

};

const ViewHeader = ({children}) => {

    let num = React.Children.count(children);

    if (num == 1) {
        return (
            <div className="view-header">
                <div className="container-fluid">
                    <div className="row">
                        <div className="col-md-12">
                            {children}
                        </div>
                    </div>
                </div>
            </div>
        );
    } else if (num == 2) {
        return (
            <div className="view-header">
                <div className="container-fluid">
                    <div className="row">
                        <div className="col-sm-8">
                            {children[0]}
                        </div>
                        <div className="col-sm-4">
                            {children[1]}
                        </div>
                    </div>
                </div>
            </div>
        );
    }

};

const ViewBody = ({children}) => {

    let num = React.Children.count(children);

    if (num == 1) {

        return <div className="view-body p-center">
                    {children}
                </div>;

    } else if (num == 2) {
        let leftPanel = children[0].type.name;

        if (leftPanel == 'Panel') {

            return (
                <div className="view-body">
                    <div className="view-left">
                        {children[0]}
                    </div>
                    <div className="view-right">
                        {children[1]}
                    </div>
                </div>
            );

        } else if (leftPanel == 'PanelMenu') {

            return (
                <div className="view-body">
                    <div className="container-fluid">
                        <div className="row">
                            <div className="col-sm-3">
                                <div className="p-menu">
                                    {children[0]}
                                </div>
                            </div>
                            <div className="col-sm-6">
                                <div className="p-center">
                                    {children[1]}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            );

        }
    } else {
        return (
            <div className="view-body p-center">
                not supported (too many children)
            </div>
        );
    }
    
};

const Panel = ({children}) =>
    <div className="container-fluid">
        <div className="row">
            <div className="col-md-12">
                {children}
            </div>
        </div>
    </div>;

export { View, ViewHeader, ViewBody, Panel };