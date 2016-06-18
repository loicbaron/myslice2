import React from 'react';

class ElementStatus extends React.Component {

    render() {
        var status = this.props.status.toLowerCase() || '';
        var iconClass = 'fa fa-lg fa-';


        switch(status) {
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

        iconClass += ' ' + status + ' fa-fw';

        return (
                <div className="elementStatus">
                    {status}&nbsp;<i className={iconClass}></i>
                </div>
        );

    }
}

export default ElementStatus;