import React from 'react';

import { NotifyInfo, NotifySuccess, NotifyError, NotifyWarning  } from './Notification';

const View = ({children, notification}) => {

    let num = React.Children.count(children);
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


    if (num == 1) {

        return <div className="p-center">
                    {children}
                    {notificationElement}
                </div>;

    } else if (num == 2) {
        let leftPanel = children[0].type.name;

        if (leftPanel == 'Panel') {
            return <div className="row">
                    <div className="col-sm-6">
                        <div className="p-left">
                            {children[0]}
                        </div>
                    </div>
                    <div className="col-sm-6">
                         <div className="p-right">
                             {children[1]}
                         </div>
                    </div>
                    {notificationElement}
                </div>;
        } else if (leftPanel == 'PanelMenu') {
            return <div className="row">
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
                {notificationElement}
            </div>

        }
    } else {
        return (
                <div className="p-center">
                    not supported (too many children)
                </div>
        );
    }
    
};

export default View;