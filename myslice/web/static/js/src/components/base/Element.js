import React from 'react';

const Element = (props) => {

    var className = 'elementBox';
    var arrow = null;
    var style;
    if(props.minHeight){
        style=props.minHeight;
    }

    if (props.type) {
        className += ' ' + props.type;
    }

    if (props.setCurrent) {
        className += ' pointer';

        if (props.element == props.current) {
            className += ' selected';
            arrow = <i className="fa fa-arrow-right fa-lg arrow-right"></i>
        }

        return (
            <li className={className} onClick={() => props.setCurrent(props.element)} style={style}>
                {props.children}
                {arrow}
            </li>
        );
    } else {
        return (
            <li className={className} style={style}>
                {props.children}
            </li>
        );
    }
};

Element.propTypes = {
    element: React.PropTypes.object.isRequired,
    type: React.PropTypes.string,
    current: React.PropTypes.object,
    setCurrent: React.PropTypes.func
};

Element.defaultProps = {
    type: null,
    current: null
};

export default Element;
