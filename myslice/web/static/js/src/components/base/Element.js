import React from 'react';
import Icon from './Icon';

class Element extends React.Component {

    constructor(props) {
        super(props);
    }

    componentDidMount() {

    }

    shouldComponentUpdate(nextProps, nextState) {
        return this.props.isSelected !== nextProps.isSelected;
    }

    renderIcon() {
        var icon = this.props.icon;

        if (icon) {
            return (
                <div className={"elementIcon " + icon}>
                    <Icon name={icon} size="2x"/>
                </div>
            );
        }
    }

    renderIconSelected() {
        if (this.props.isSelected) {
            switch (this.props.iconSelected) {
                case 'arrow':
                    return <i className="fa fa-arrow-right fa-lg arrow-right"></i>;
                    break;
                case 'check':
                    return <i className="fa fa-check-square-o fa-lg check-right"></i>;
                    break;
            }
        }
    }

    renderMenu() {
        var rMenu = null;
        if (this.props.options) {
            rMenu =  this.props.options.map((option) => {
                        return option;
                    });
        }
        return rMenu;
    }
    renderStatus() {
        var status = this.props.element.status || this.props.status || null;
        if(typeof(status) === 'object'){
            if(status['online']){
                status = 'online';
            }else{
                status = 'offline';
            }
        }
        var rStatus = null;
        if (status) {
           rStatus = <div className="elementStatus">
               <Icon name={status} />&nbsp;{status}
           </div>;
        }
        return rStatus;
    }
    render() {
        var className = 'elementBox';
        var style;
        var callback = null;
        var options = this.props.options;
        var status = this.props.status;
        if (this.props.type) {
            className += ' ' + this.props.type;
        }

        if (this.props.handleSelect) {
            callback = () => this.props.handleSelect(this.props.element);
            className += ' pointer';
        }

        if (this.props.isSelected) {
            className += ' selected';
        }

        return (
            <li className={className} onClick={callback} style={this.props.minHeight}>
                {this.renderIcon()}

                <div className="elementMenu">
                {this.renderStatus()}
                {this.renderMenu()}
                </div>
                {this.props.children}
                {this.renderIconSelected()}
            </li>
        );
    }
};

Element.propTypes = {
    element: React.PropTypes.object.isRequired,
    type: React.PropTypes.string,
    icon: React.PropTypes.string,
    iconSelected: React.PropTypes.string,
    isSelected: React.PropTypes.bool,
    handleSelect: React.PropTypes.func
};

Element.defaultProps = {
    type: null,
    icon: null,
    iconSelected: 'check',
    isSelected: false,
    status: null,
    options: [],
};

export { Element };
