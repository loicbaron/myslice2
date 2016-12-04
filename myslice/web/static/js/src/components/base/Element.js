import React from 'react';
import { Icon } from './Icon';

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
        let icon = this.props.icon || this.props.type;

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

    renderOptions() {
        let status = this.props.status || this.props.element.status || null;
        let rStatus = null;
        let rOptions = null;

        if (status) {
            rStatus = <div className="elementStatus">
                <Icon name={status} />&nbsp;{status}
            </div>;
        }

        if (this.props.options) {
            rOptions = this.props.options.map(function(option, i) {
                if ((typeof option.label !== "undefined") && (typeof option.callback !== "undefined")) {
                    return <div key={i} className={ "elementOption " + option.label }
                                onClick={() => option.callback(this.props.element) }>
                        <Icon name={option.label} />{option.label}
                    </div>;
                }
            }.bind(this));
        }

        return <div className="elementOptions">
            {rStatus}
            {rOptions}
        </div>;
    }
    render() {
        let className = 'elementBox';
        let style;
        let callback = null;

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
                {this.renderOptions()}
                {this.props.children}
                {this.renderIconSelected()}
            </li>
        );
    }
}

Element.propTypes = {
    element: React.PropTypes.object.isRequired,
    type: React.PropTypes.string,
    icon: React.PropTypes.string,
    iconSelected: React.PropTypes.string,
    isSelected: React.PropTypes.bool,
    handleSelect: React.PropTypes.func,
    status: React.PropTypes.string,
    options: React.PropTypes.array
};

Element.defaultProps = {
    type: null,
    icon: null,
    iconSelected: 'check',
    isSelected: false,
    handleSelect: () => { return null; },
    status: null,
    options: [],
};

export { Element };
