import React from 'react';

import store from '../../stores/base/ViewStore';
import actions from '../../actions/base/ViewActions';

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

    handleClick(event) {
        if (this.state.selectedElement === this.props.element) {
            actions.updateSelectedElement(null);
        } else {
            actions.updateSelectedElement(this.props.element);
        }

    }

    render() {
        var type = this.props.type || '';
        if (this.state.selectedElement === this.props.element) {
            var className = 'elementBox selected ' + type;
        } else {
            var className = 'elementBox';
        }

        return (
            <li className={className} onClick={this.handleClick}>
                {this.props.children}
            </li>
        );
    }
}

export default Element;