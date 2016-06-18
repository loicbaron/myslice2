import React from 'react';

class ElementStatus extends React.Component {

    render() {
        var status = this.props.status.toLowerCase() || '';
        var iconClass = 'fa fa-';


        switch(status) {
            case 'enabled':
            case 'success':
                iconClass += 'check';
                break;
            case 'new':
                iconClass += 'cog';
                break;
            case 'waiting':
                iconClass += 'clock-o';
                break;
            case 'running':
                iconClass += 'cog fa-spin fa-fw';
                break;
            case 'warning':
            case 'error':
                iconClass += 'exclamation';
                break;
            default:
                iconClass += 'question';
                break;
        }

        iconClass += ' ' + status;

        return (
                <div className="elementStatus">
                    {status}&nbsp;<i className={iconClass}></i>
                </div>
        );

    }
}

export default ElementStatus;