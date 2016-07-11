import React from 'react';

import store from '../../stores/NavBarStore';
import actions from '../../actions/NavBarActions';


class SlicesMenuEntry extends React.Component {

    constructor(props) {
        super(props);
        this.handleClick = this.handleClick.bind(this);
    }

    sliceLabel() {
        return (this.props.slice.name || this.props.slice.shortname);
    }

    projectLabel() {
        return this.props.slice.project.name || this.props.slice.project.shortname;
    }

    handleClick() {
        window.location.href = "/slices/" + this.props.slice.hrn;
    }

    render() {
        var className = "slice-menu-entry";
        if (this.props.current) {
            className += " active";
        }

        return (<li className={className} onClick={this.handleClick}>
                    <h5><i className="fa fa-flask"></i> {this.projectLabel()}</h5>
                    <h4>{this.sliceLabel()}</h4>
                    <span>{this.props.slice.shortname}</span>
                </li>);

    }
}

SlicesMenuEntry.propTypes = {
    slice: React.PropTypes.object.isRequired,
    active: React.PropTypes.bool
};

SlicesMenuEntry.defaultProps = {
    active: false
};

class SlicesMenuButton extends React.Component {

    constructor(props) {
        super(props);
    }

    showMenu() {
        console.log('hello')
        actions.showMenu(true);
    }

    render() {
        var url = "/slices/" + this.props.currentSlice.hrn;
        if (this.props.currentSlice) {
            return (<a href={url} onMouseEnter={this.showMenu}>
                        <i className="fa fa-tasks fa-lg"></i> {this.props.currentSlice.shortname}
                    </a>);
        }
    }
}



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
            menu = (<div className="slices-menu" onMouseLeave={this.hideMenu} onMouseEnter={this.showMenu}>
                        <ul>
                            {
                                this.state.slices.map(function(slice) {
                                    let current = this.state.currentSlice.id === slice.id;
                                    return <SlicesMenuEntry key={slice.id} slice={slice} current={current} />
                                }.bind(this))
                            }
                        </ul>
                    </div>);

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