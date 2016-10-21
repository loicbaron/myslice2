import React from 'react';

const ElementStatus = ({status}) => {

        if(status === undefined ){
            status = '';
        }
        var elementStatus = status.toLowerCase() || '';
        
        var iconClass = 'fa fa-lg fa-';

        switch(elementStatus) {
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

        iconClass += ' ' + elementStatus + ' fa-fw';

        return (
                <div className="elementStatus">
                    <i className={iconClass}></i>&nbsp;{elementStatus}
                </div>
        );

};

export default ElementStatus;
