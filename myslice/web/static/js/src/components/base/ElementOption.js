import React from 'react';

const ElementOption = ({label, handleClick}) => {

        var elementOption = label.toLowerCase() || '';
        var iconClass = 'fa fa-lg fa-';

        switch(elementOption) {
            case 'delete':
                iconClass += 'delete';
                break;
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
            default:
                iconClass += 'question';
                break;
        }

        iconClass += ' ' + elementOption + ' fa-fw';
        var className = 'elementOption ' + elementOption;
        return (
                <div className={className}>
                    <i className={iconClass}></i>&nbsp;{elementOption}
                </div>
        );

};

export default ElementOption;