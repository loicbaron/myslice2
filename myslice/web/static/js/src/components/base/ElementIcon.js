import React from 'react';

const ElementIcon = ({icon}) => {

        var iconClass = 'fa fa-';
        var divClass = 'elementIcon';
    
        switch(icon) {
            case 'project':
                iconClass += 'flask';
                break;
            case 'user':
                iconClass += 'user';
                break;
            case 'slice':
                iconClass += 'tasks';
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
            default:
                iconClass += 'question';
                break;
        }

        iconClass += ' ' + icon + ' fa-2x';
        divClass += ' ' + icon;

        return (
            <div className={divClass}>
                <i className={iconClass}></i>
            </div>
        );
};

export default ElementIcon;