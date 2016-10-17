import React from 'react';

const Element = (props) => {

    var className = 'elementBox';
    var style;
    var callback = null;

    if (props.minHeight) {
        style = props.minHeight;
    }

    if (props.type) {
        className += ' ' + props.type;
    }

    if (props.handleClick) {
        callback = () => props.handleClick(props.element);
        className += ' pointer';
    }

    if ((typeof(props.element.isCurrent) === 'boolean' && (props.element.isCurrent))) {
        className += ' selected';
        return (
            <li className={className} onClick={callback} style={style}>
                {props.children}
                <i className="fa fa-arrow-right fa-lg arrow-right"></i>
            </li>
        );
    }

    if ((typeof(props.element.isSelected) === 'boolean' && (props.element.isSelected))) {
        className += ' selected';
        return (
            <li className={className} onClick={callback} style={style}>
                {props.children}
                <i className="fa fa-check-square-o fa-lg check-right"></i>
            </li>
        );
    }

    return (
        <li className={className} onClick={callback} style={style}>
            {props.children}
        </li>
    );
};

Element.propTypes = {
    element: React.PropTypes.object.isRequired,
    type: React.PropTypes.string,
    isSelected: React.PropTypes.bool,
    isChecked: React.PropTypes.bool,
    handleClick: React.PropTypes.func
};

Element.defaultProps = {
    type: null,
    current: null
};

export default Element;
