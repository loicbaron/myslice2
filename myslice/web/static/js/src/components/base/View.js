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

const Panel = ({children, single}) => {

    if (single) {
        return (
            <div className="container-fluid">
                <div className="row">
                    <div className="col-sm-6 col-sm-offset-3">
                        {children}
                    </div>
                </div>
            </div>
        )
    } else {
        return (
            <div className="container-fluid">
                <div className="row">
                    <div className="col-sm-12">
                        {children}
                    </div>
                </div>
            </div>
        );
    }
}

Panel.propTypes = {
    single: React.PropTypes.bool
};

Panel.defaultProps = {
    single: false
};

const PanelMenu = ({children}) =>
    <ul>{children}</ul>;

class PanelMenuEntry extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            'selected': false
        };
        this.handleSelect = this.handleSelect.bind(this)
    }

    handleSelect() {
        let name = this.props.name;
        this.props.handleSelect(name);
    }

    render() {

        let icon = this.props.icon || 'dot-circle-o';
        let iconClass = 'fa fa-' + icon + ' fa-lg';
        let entryClass = '';

        return (
            <li>
                <span>
                    <i className={iconClass}></i>
                    <a className={entryClass} onClick={this.handleSelect}>{this.props.children}</a>
                </span>
            </li>
        );
    }

}

PanelMenuEntry.propTypes = {
    name: React.PropTypes.string.isRequired,
    icon: React.PropTypes.string,
    handleSelect: React.PropTypes.func.isRequired,
};

export { View, ViewHeader, ViewBody, Panel, PanelMenu, PanelMenuEntry };