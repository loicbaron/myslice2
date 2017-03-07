import React from 'react';
import { Icon } from './Icon';

class Element extends React.Component {

    constructor(props) {
        super(props);
    }

    componentDidMount() {

    }

    shouldComponentUpdate(nextProps, nextState) {
        //return this.props.isSelected !== nextProps.isSelected;
        return true;
    }

    renderIcon() {
        let icon = this.props.type;

        if (icon) {
            return (
                <div className={"elementIcon " + icon}>
                    <Icon name={icon} size="2x" circle={true} />
                </div>
            );
        }
    }

    renderIconSelected() {
        switch (this.props.isSelected) {
            case "arrow":
                return <i className="fa fa-arrow-right fa-lg arrow-right"></i>;
                break;
            case "check":
                return <i className="fa fa-check-square-o fa-lg check-right"></i>;
                break;
        }
    }

    renderTitle() {
        let title = this.props.element.label || this.props.element.name || this.props.element.shortname;
        let subtitle = title;
        return <h3 className="elementTitle">
                    {title} &nbsp; <span>{subtitle}</span>
                </h3>
    }

    render() {
        let className = 'elementBox';
        let callback = null;

        if (this.props.type) {
            className += ' ' + this.props.type;
        }

        if (this.props.handleSelect) {
            callback = () => this.props.handleSelect(this.props.element);
            className += ' pointer';
        } else {

        }

        if (this.props.isSelected) {
            className += ' selected';
        }

        return (
            <li className={className} onClick={callback} style={this.props.minHeight}>
                {this.renderTitle()}
                {this.renderIcon()}
                {this.props.children}
                {this.renderIconSelected()}
                <div className="elementOptions">
                    <ElementOptions element={this.props.element}
                                    status={this.props.status}
                                    options={this.props.options} />
                </div>
            </li>
        );
    }
}

Element.propTypes = {
    element: React.PropTypes.object.isRequired,
    type: React.PropTypes.string,
    icon: React.PropTypes.string,
    isSelected: React.PropTypes.string,
    handleSelect: React.PropTypes.func,
    status: React.PropTypes.string,
    options: React.PropTypes.array,
    details: React.PropTypes.array
};

Element.defaultProps = {
    type: null,
    icon: null,
    isSelected: null,
    handleSelect: () => { return null; },
    status: null,
    options: [],
    details: []
};

const ElementOptions = ({element, status, options}) => {
    let oStatus = status || element.status || null;
    let rStatus = null;
    let rOptions = null;

    if (oStatus) {
        rStatus = <li className="elementStatus">
            <Icon name={oStatus} />&nbsp;{oStatus}
        </li>;
    }

    if (options) {
        rOptions = options.map((option, i) => {
            if (typeof option.callback !== "undefined") {
                let oOption = option.icon || option.label;
                return <li key={i} className={ "elementOption " + oOption }
                            onClick={() => option.callback(element) }>
                    <Icon name={oOption} />{option.label}
                </li>;
            }
        });
    }

    return <ul>
        {rOptions}
        {rStatus}
    </ul>;
};

ElementOptions.propTypes = {
    element: React.PropTypes.object.isRequired,
    status: React.PropTypes.string,
    options: React.PropTypes.array
};

ElementOptions.defaultProps = {
    status: null,
    options: []
};

class ElementDetails extends React.Component {

    constructor(props) {
        super(props);
        this.state = { details: false };
        this.handleDetails = this.handleDetails.bind(this);
    }

    handleDetails() {
        this.setState({details: !this.state.details});
    }

    render() {
        if (this.state.details) {
            return (
                <div>
                    <div className="elementDetailsLink" onClick={this.handleDetails}>
                        <i className="fa fa-caret-up" />
                        <span className="less">hide details</span>
                    </div>
                    <div className="elementDetails">
                        {this.props.children}
                    </div>
                </div>
            );
        } else {
            return (
                <div className="elementDetailsLink" onClick={this.handleDetails}>
                    <i className="fa fa-caret-down" />
                    <span className="more">show more details</span>
                    <span className="elementDetailsText">{this.props.text}</span>
                </div>
            );
        }
    }
}
ElementDetails.propTypes = {
    text: React.PropTypes.string
};

ElementDetails.defaultProps = {
    text: null
};


const ElementSummary = ({elements, type, options}) => {
    let elementList = <ul><li>No elements found</li></ul>;

    if (elements.length > 0) {
        elementList = <ul>
            {
                elements.map((element) =>
                    <li className="summaryBox" key={element.id}>
                        {element.name || element.shortname}
                        <ElementOptions element={element} options={options} />
                    </li>
                )
            }
        </ul>;
    }
    return <div className={"summaryList " + type }>
        <div className={"elementIcon summaryIcon " + type}>
            <Icon name={type} circle={true} />
        </div>
        {elementList}
    </div>;
};

ElementSummary.propTypes = {
    elements: React.PropTypes.array.isRequired,
    type: React.PropTypes.string.isRequired,
    options: React.PropTypes.array
};

ElementSummary.defaultProps = {
    options: []
};


export { Element, ElementDetails, ElementSummary, ElementOptions };
