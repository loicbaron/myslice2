import React from 'react';

const Icon = ({name, size, circle}) => {
    let icon;

    if (name) {
        icon = name.toLowerCase()
    }

    let iconClass = 'fa fa-';

    switch(icon) {
        case 'approved':
        case 'enabled':
        case 'success':
        case 'online':
            iconClass += 'check';
            break;
        case 'new':
            iconClass += 'cog';
            break;
        case 'pending':
            iconClass += 'clock-o';
            break;
        case 'denied':
            iconClass += 'times';
            break;
        case 'waiting':
            iconClass += 'clock-o';
            break;
        case 'running':
            iconClass += 'cog fa-spin ';
            break;
        case 'warning':
        case 'error':
        case 'offline':
            iconClass += 'exclamation';
            break;
        case 'info':
            iconClass += 'info';
            break;
        case 'project':
            iconClass += 'flask';
            break;
        case 'user':
            iconClass += 'user';
            break;
        case 'slice':
            iconClass += 'tasks';
            break;
        case 'lease':
            iconClass += 'calendar';
            break;
        case 'resource':
            iconClass += 'server';
            break;
        case 'authority':
            iconClass += 'institution';
            break;
        case 'testbed':
            iconClass += 'cube';
            break;
        case 'registry':
            iconClass += 'building';
            break;
        case 'delete':
            iconClass += 'trash';
            break;
        case 'add':
        case 'create':
            iconClass += 'plus-circle';
            break;
        case 'remove':
            iconClass += 'minus-circle';
            break;
        default:
            iconClass += 'question';
            break;
    }

    iconClass += ' ' + icon + ' fa-fw';

    let sizeClass = null;
    if (typeof size !== undefined) {
        switch(size) {
            default:
            case 'lg':
                sizeClass = 'fa-lg';
                break;
            case '2x':
                sizeClass = 'fa-2x';
                break;
            case '3x':
                sizeClass = 'fa-3x';
                break;
        }
    }

    if (circle) {
        return (
            <span className={"fa-stack " + sizeClass}>
                  <i className="fa fa-circle fa-stack-2x" />
                  <i className={iconClass + " fa-stack-1x fa-inverse"} />
            </span>
        );
    } else {
        return <i className={iconClass} />;
    }


};

Icon.propTypes = {
    name: React.PropTypes.string,
    size: React.PropTypes.string,
    circle: React.PropTypes.bool
};

Icon.defaultProps = {
    size: 'lg',
    circle: false
};

export { Icon };
