import React from 'react';

const ElementStatus = ({status}) => {

        var elementStatus = status.toLowerCase() || '';
        var iconClass = 'fa fa-lg fa-';

        switch(elementStatus) {
            case 'approved':
            case 'enabled':
            case 'success':
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
                iconClass += 'exclamation';
                break;
            default:
                iconClass += 'question';
                break;
        }

        iconClass += ' ' + elementStatus + ' fa-fw';

        return (
                <div className="elementStatus">
                    {elementStatus}&nbsp;<i className={iconClass}></i>
                </div>
        );

};

export default ElementStatus;