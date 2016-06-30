import React from 'react';

import store from '../../stores/NavBarStore';
import actions from '../../actions/NavBarActions';


class SlicesMenuEntry extends React.Component {

    constructor(props) {
        super(props);
    }

    sliceLabel() {
        return (this.props.slice.name || this.props.slice.shortname);
    }

    projectLabel() {
        return this.props.slice.project.name || this.props.slice.project.shortname;
    }

    static setCurrentSlice(slice) {
        actions.setCurrentSlice(slice);
        //window.location.href = "/slices/" + slice.hrn;
    }

    render() {

        return <li className="slice-menu-entry" onClick={this.setCurrentSlice}>
            <h5><i className="fa fa-flask"></i> {this.projectLabel()}</h5>
            <h4>{this.sliceLabel()}</h4>
            <span>{this.props.slice.shortname}</span>
        </li>;

    }
}

SlicesMenuEntry.propTypes = {
    slice: React.PropTypes.object.isRequired
};

SlicesMenuEntry.defaultProps = {
};


class SlicesMenu extends React.Component {

    constructor(props) {
        super(props);
        this.state =  store.getState();
        this.onChange = this.onChange.bind(this);
        this.showMenu = this.showMenu.bind(this);
        this.hideMenu = this.hideMenu.bind(this);
    }

    componentWillMount() {

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

    render() {
        if (!this.state.slice) {
            //console.log(this.state.slices)
            //actions.setCurrentSlice(this.state.slices[0])
        }
        //console.log(this.state.current);
        var menuBox = null;

        if (this.state.slices.length) {
            var menu = this.state.slices.map(function(slice) {
                return <SlicesMenuEntry key={slice.id} slice={slice}>
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