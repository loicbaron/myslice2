import React from 'react';

class PanelMenuEntry extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            'selected': false
        };
        this.handleSelect = this.handleSelect.bind(this)
    }

    handleSelect() {
        var name = this.props.name;
        this.props.handleSelect(name);
    }

    render() {

        var icon = this.props.icon || 'dot-circle-o';
        var iconClass = 'fa fa-' + icon + ' fa-lg';
        var entryClass = '';
        
        return (
            <li>
                <span>
                    <i className={iconClass}></i>
                    <a className={entryClass} onClick={this.handleSelect}>{this.props.children}</a>
                </span>
            </li>
        );
    }

}

PanelMenuEntry.propTypes = {
    name: React.PropTypes.string.isRequired,
    icon: React.PropTypes.string,
    handleSelect: React.PropTypes.func.isRequired,
};

export default PanelMenuEntry;