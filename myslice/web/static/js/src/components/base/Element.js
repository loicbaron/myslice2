import React from 'react';

class Element extends React.Component {

    constructor(props) {
        super(props);
        this.handleClick = this.handleClick.bind(this);
    }

    componentDidMount() {
        if (typeof(this.props.selectElement) != 'undefined') {

        }
    }

    handleClick() {
        if (this.props.selectElement && (this.props.element != this.props.selected)) {
            this.props.selectElement(this.props.element);
        } else {
            this.props.selectElement(null);
        }
    }

    render() {
        var className = 'elementBox';

        if (this.props.type) {
            className += ' ' + this.props.type;
        }

        if (!this.props.selectElement) {
            return (
                <li className={className}>
                    {this.props.children}
                </li>
            );
        } else {
            className += ' pointer';

            if (this.props.element == this.props.selected) {
                className += ' selected';
            }

            return (
                <li className={className} onClick={this.handleClick}>
                    {this.props.children}
                </li>
            );
        }

    }
}

Element.propTypes = {
    element: React.PropTypes.object.isRequired,
    type: React.PropTypes.string,
    selected: React.PropTypes.object,
    selectElement: React.PropTypes.func
};

Element.defaultProps = {
    selected: null,
    selectElement: null
};

export default Element;