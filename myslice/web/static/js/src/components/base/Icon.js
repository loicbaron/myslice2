import React from 'react';

const Icon = ({name, size}) => {
    let icon;

    if (name) {
        icon = name.toLowerCase()
    }

    let iconClass = 'fa fa-lg fa-';

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

    if (typeof size !== undefined) {
        switch(size) {
            case 'lg':
                iconClass += ' fa-lg';
                break;
            case '2x':
                iconClass += ' fa-2x';
                break;
            case '3x':
                iconClass += ' fa-3x';
                break;
        }
    }

    return <i className={iconClass} />;
};

export { Icon };
