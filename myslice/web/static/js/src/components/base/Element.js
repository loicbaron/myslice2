import React from 'react';

import store from '../../stores/base/ElementStore';
import actions from '../../actions/base/ElementActions';

class Element extends React.Component {

    constructor(props) {
        super(props);
        this.state = store.getState();
        this.onChange = this.onChange.bind(this);
        this.handleClick = this.handleClick.bind(this);
    }

    componentDidMount() {
        store.listen(this.onChange);
    }

    componentWillUnmount() {
        store.unlisten(this.onChange);
    }

    onChange(state) {
        this.setState(state);
    }

    handleClick() {
        actions.selectElement(this.props.element);
    }

    render() {
        var className = 'elementBox';

        if (this.props.type) {
            className += ' ' + this.props.type;
        }

        if (this.props.select) {
            className += ' pointer';

            if (this.props.element == this.state.selected) {
                className += ' selected';
            }

            return (
                <li className={className} onClick={this.handleClick}>
                    {this.props.children}
                </li>
            );
        } else {
            return (
                <li className={className}>
                    {this.props.children}
                </li>
            );
        }

    }
}

Element.propTypes = {
    element: React.PropTypes.object.isRequired,
    type: React.PropTypes.string,
    select: React.PropTypes.bool
};

Element.defaultProps = {
    select: false
};

export default Element;