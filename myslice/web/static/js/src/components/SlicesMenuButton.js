import React from 'react';

import store from '../stores/SlicesStore';
import actions from '../actions/SlicesActions';

class SlicesMenu extends React.Component {

    constructor(props) {
        super(props);
        this.state =  store.getState();
        this.onChange = this.onChange.bind(this);
        this.setCurrentSlice = this.setCurrentSlice.bind(this);
    }

    componentDidMount() {
        store.listen(this.onChange);

        actions.fetchSlices({});

    }

    componentWillUnmount() {
        store.unlisten(this.onChange);
    }

    onChange(state) {
        this.setState(state);
    }

    showMenu() {
        actions.showMenu(true);
    }

    setCurrentSlice(slice) {
        actions.setCurrentSlice(slice);
        window.location.href = "/slices/" + slice.hrn;
    }

    render() {
        if (!this.state.current.slice) {
            //console.log(this.state.slices)
            //actions.setCurrentSlice(this.state.slices[0])
        }

        return (
            <a onMouseEnter={this.showMenu} href="#">
                <i className="fa fa-tasks fa-lg"></i> {this.state.current.slice.shortname} <span className="caret"></span>
            </a>
        );

    }
}

SlicesMenu.propTypes = {
    // slices: React.PropTypes.object.isRequired,
};

SlicesMenu.defaultProps = {
};

export default SlicesMenu;