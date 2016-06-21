import React from 'react';

class Visibility extends React.Component {

    render() {
        var type = this.props.type || '';
        var label = type.charAt(0).toUpperCase() + type.slice(1);
        var iconClass = 'fa fa-';


        switch(type) {
            case 'public':
                iconClass += 'globe';
                break;
            case 'authority':
                iconClass += 'building';
                break;
            case 'private':
                iconClass += 'lock';
                break;
        }

        iconClass += ' ' + icon + ' fa-lg fa-fw';

        return (
            <div className="visibility">
                <i className={iconClass}></i> {label}
            </div>
        );
  }
}

export default Visibility;