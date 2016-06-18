import React from 'react';

class ElementIcon extends React.Component {

    render() {
        var icon = this.props.icon || '';
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
                iconClass += 'server';
                break;
            case 'resource':
                iconClass += 'server';
                break;
            case 'authority':
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
  }
}

export default ElementIcon;