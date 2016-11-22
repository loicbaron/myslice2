import React from 'react';

import store from '../../stores/NavBarStore';
import actions from '../../actions/NavBarActions';

const ProjectMenuEntry = ({project, slices}) =>{
    return (<li key={project}>
            <h4><i className="fa fa-flask"></i> {project}</h4>
            {
            slices.map(function(slice){
                //let active = this.state.currentSlice.id === slice.id;
                let active = false;
                return <SlicesMenuEntry key={slice.id} slice={slice} active={active} />
            }.bind(this))
            }
            </li>);
};

ProjectMenuEntry.propTypes = {
    slices: React.PropTypes.array.isRequired,
    project: React.PropTypes.oneOfType([
    React.PropTypes.string,
    React.PropTypes.number])
};

const SlicesMenuEntry = ({slice, active}) => {
    var sliceLabel = slice.name || slice.shortname;
    var projectLabel = slice.project.name || slice.project.shortname;
    var className = "col-md-4";
    var style = {'paddingBottom':'5px'};

    if (active) {
        className += " active";
    }

    if (!projectLabel) {
        return (<div className={className} style={style}>
                <h5 onClick={() => window.location.href = "/slices/" + slice.hrn}><i className="fa fa-tasks fa-lg"></i>{sliceLabel}</h5>
        </div> );
    } else {
        return (<div className={className} style={style}>
                <h5 onClick={() => window.location.href = "/slices/" + slice.hrn}><i className="fa fa-tasks fa-lg"></i>{sliceLabel}</h5>
        </div>);
    }
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
    else
    {
        return ( <div>No slices </div>)
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
        var project_slices = Array();
        for(var i in this.state.slices){
            var s = this.state.slices[i];
            if (s.project.shortname === undefined){
                var p = "No Project";
            }else{
                var p = s.project.shortname.toString();
            }
            if(project_slices.hasOwnProperty(p)){
                project_slices[p].push(s);
            }else{
                project_slices[p] = [s];
            }
        }
        var items = [];
        for(var project in project_slices){
            var slices = project_slices[project];
            var item = <ProjectMenuEntry key={project} project={project} slices={slices} />
            items.push(item);
        }
        if(this.state.slices.length==0){
            item = <div key='0'><a href="/projects">You have no Slice <br/> Create one in a Project</a></div>;
            items.push(item);
        }
        if (this.state.slicesMenu) {
            var padding={'padding':'10px'};
            menu = <div className="slices-menu" onMouseLeave={this.hideMenu} onMouseEnter={this.showMenu}>
                        <div style={padding}>
                            <ul>
                            {
                            items.map(function(item){
                                return item;
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
