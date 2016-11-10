import React from 'react';

import List from '../base/List';
import Element from '../base/Element';
import ElementTitle from '../base/ElementTitle';
import ElementId from '../base/ElementId';
import DateTime from '../base/DateTime';
import DeleteProject from '../DeleteProject';

class ProjectElement extends React.Component {

    render() {
        var label = this.props.project.name || this.props.project.shortname;
        var authority = this.props.project.authority.name || this.props.project.authority.shortname;
        var button;
        var minHeight;
        var topPosition;
        if(this.props.removeProject){
            minHeight = {'minHeight':'100px'};
            topPosition = {'top':'60px'};
            button = <DeleteProject project={this.props.project} topPosition={topPosition} />
        }
        var users;
        if(this.props.project.pi_users){
            users = <span className="elementLabel">Users {this.props.project.pi_users.length} </span>
        }
        var slices;
        if(this.props.project.slices){
            slices = <span className="elementLabel">Slices: {this.props.project.slices.length}</span>
        }
        var slicesInDashboard;
        if(this.props.project.slices){
            var slicesInDashboard = <div>
            {
                this.props.project.slices.map(function (slice) {
                    var slice_link="/slices/"+slice.hrn;
                    return <span key={slice.id } className="elementLabel"><i className="fa fa-tasks fa-lg"></i>&nbsp;<a href={slice_link}>{slice.shortname}</a>&nbsp;</span>;
                }.bind(this))
            }
            </div>;
            //slicesInDashboard = <span className="elementLabel">Slices: {SliceLabel}</span>
        }
        var created;
        if(this.props.project.created){
            created = <div className="col-sm-3"><DateTime label="Created" timestamp={this.props.project.created}/></div>
        }
        var enabled;
        if(this.props.project.enabled){
            created = <div className="col-sm-3"><DateTime label="Enabled" timestamp={this.props.project.enabled}/></div>
        }
        var updated;
        if(this.props.project.updated){
            created = <div className="col-sm-3"><DateTime label="Updated" timestamp={this.props.project.updated}/></div>
        }
        var authorityElement;
        if(authority){
            authorityElement = <span className="elementLabel">Managed by {authority}</span>
        }
        var projectElements;
        if(users || slices || authorityElement){
            projectElements = <div className="elementDetail">{users}&nbsp;&nbsp;{slices}<br/>{authorityElement}</div>
        }
        var options = [];
        if (this.props.detailed) {
            return (
                <Element element={this.props.project}
                         type="project"
                         handleSelect={this.props.handleSelect}
                         minHeight={minHeight}
                         status={this.props.project.status}
                         options={options}
                         icon="project"
                >
                    <ElementTitle label={label} detail={this.props.project.shortname}/>
                    <ElementId id={this.props.project.id}/>
                    {button}
                    {projectElements}
                    <div className="row elementDate">
                        {created}
                        {enabled}
                        {updated}
                    </div>
                </Element>
            );
        }
        else
            {
            return (
                <Element element={this.props.project} type="project" handleClick={this.props.handleClick} minHeight={minHeight} icon="project">

                    <a href="/projects"><ElementTitle label={label} detail={this.props.project.shortname} /></a>

                    <ElementId id={this.props.project.id} />

                    <div> {slicesInDashboard}</div>

                </Element>
            );
        }

    }
}

ProjectElement.propTypes = {
    project: React.PropTypes.object.isRequired,
    handleClick: React.PropTypes.func,
    removeProject: React.PropTypes.bool,
    detailed: React.PropTypes.bool,
};

ProjectElement.defaultProps = {
    removeProject: true,
    detailed: true,
};



class ProjectList extends React.Component {

    render() {

        if (!this.props.projects || this.props.projects.length==0) {
            return <List>No project</List>
        } else {
            return (
                <List detailed={ this.props.detailed}>
                {
                    this.props.projects.map(function(project) {
                        return <ProjectElement key={project.id} project={project} detailed={this.props.detailed} handleSelect={this.props.handleSelect} />;
                    }.bind(this))
                }
                </List>
            );
        }

    }
}

ProjectList.propTypes = {
    projects: React.PropTypes.array.isRequired,
    handleClick: React.PropTypes.func,
    detailed: React.PropTypes.bool,
};

ProjectList.defaultProps = {
};

export { ProjectElement, ProjectList };
