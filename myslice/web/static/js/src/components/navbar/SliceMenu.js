import React from 'react';

import store from '../../stores/NavBarStore';
import actions from '../../actions/NavBarActions';


const SlicesMenuEntry = ({slice, active}) => {
    var sliceLabel = slice.name || slice.shortname;
    var projectLabel = slice.project.name || slice.project.shortname;
    var className = "slice-menu-entry";

    if (active) {
        className += " active";
    }

    return (<li className={className} onClick={() => window.location.href = "/slices/" + slice.hrn}>
                <h5><i className="fa fa-flask"></i> {projectLabel}</h5>
                <h4>{sliceLabel}</h4>
                <span>{slice.shortname}</span>
            </li>);
};

SlicesMenuEntry.propTypes = {
    slice: React.PropTypes.object.isRequired,
    active: React.PropTypes.bool
};

SlicesMenuEntry.defaultProps = {
    active: false
};

const SlicesMenuButton = ({currentSlice}) => {

    var url = "/slices/" + currentSlice.hrn;

    if (currentSlice) {
        return (<a href={url} onMouseEnter={() => actions.showMenu(true)}>
                    <i className="fa fa-tasks fa-lg"></i> {currentSlice.shortname}
                </a>);
    }
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
        store.listen(this.onChange);
        actions.fetchSlices();
    }

    componentDidMount() {

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
        var menu = null;

        if (this.state.slicesMenu) {
            menu = <div className="slices-menu" onMouseLeave={this.hideMenu} onMouseEnter={this.showMenu}>
                        <div>
                            <ul>
                                {
                                    this.state.slices.map(function(slice) {
                                        let active = this.state.currentSlice.id === slice.id;
                                        return <SlicesMenuEntry key={slice.id} slice={slice} active={active} />
                                    }.bind(this))
                                }
                            </ul>
                        </div>
                    </div>;

        }

        if (this.state.currentSlice) {
             return <div>
                        <SlicesMenuButton currentSlice={this.state.currentSlice} />
                        {menu}
                    </div>;
        } else {
            return null;
        }

    }
}

SlicesMenu.propTypes = {
};

SlicesMenu.defaultProps = {
};

export default SlicesMenu;