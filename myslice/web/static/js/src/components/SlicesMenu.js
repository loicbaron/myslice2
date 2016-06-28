import React from 'react';

import store from '../stores/SlicesStore';
import actions from '../actions/SlicesActions';

import SlicesMenuEntry from './SlicesMenuEntry';

class SlicesMenu extends React.Component {

    constructor(props) {
        super(props);
        this.state =  store.getState();
        this.onChange = this.onChange.bind(this);
        this.showMenu = this.showMenu.bind(this);
        this.hideMenu = this.hideMenu.bind(this);
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
        clearTimeout(this.menuTimer);
        actions.showMenu(true);
    }

    hideMenu() {
        this.menuTimer = setTimeout(
            function () {
                actions.showMenu(false);
            },
            500
        );

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
        //console.log(this.state.current);
        var menuBox = null;

        if (this.state.slices.length) {
            var menu = this.state.slices.map(function(slice) {
                return <SlicesMenuEntry key={slice.id} slice={slice} setCurrentSlice={this.setCurrentSlice}>
                    {slice.shortname}
                </SlicesMenuEntry>
            }.bind(this))

        }


        if (this.state.menu) {
             return <div className="slices-menu" onMouseLeave={this.hideMenu} onMouseEnter={this.showMenu}>
                    <ul>
                    {menu}
                    </ul>
            </div>;
        } else {
            return null;
        }

    }
}

SlicesMenu.propTypes = {
    // slices: React.PropTypes.object.isRequired,
};

SlicesMenu.defaultProps = {
};

export default SlicesMenu;