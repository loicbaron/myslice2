import React from 'react';

import Element from './base/Element';
import ElementTitle from './base/ElementTitle';
import ElementId from './base/ElementId';
import ElementStatus from './base/ElementStatus';
import ElementIcon from './base/ElementIcon';
import DateTime from './base/DateTime';

import DeleteProject from './DeleteProject';

class ProjectsRow extends React.Component {

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
            slices = <span className="elementLabel">Slices {this.props.project.slices.length}</span>
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
        var projectDetails;
        if(users || slices || authorityElement){
            projectDetails = <div className="elementDetail">{users}&nbsp;&nbsp;{slices}<br/>{authorityElement}</div>
        }
        return (
            <Element element={this.props.project} type="project" setCurrent={this.props.setCurrent} current={this.props.current} minHeight={minHeight}>
                <ElementStatus status={this.props.project.status}/>
                <ElementIcon icon="project"/>
                <ElementTitle label={label} detail={this.props.project.shortname}/>
                <ElementId id={this.props.project.id}/>
                {button}
                {projectDetails}
                <div className="row elementDate">
                    {created}
                    {enabled}
                    {updated}
                </div>
            </Element>
        );
    }
}

ProjectsRow.propTypes = {
    project: React.PropTypes.object.isRequired,
    current: React.PropTypes.object,
    setCurrent: React.PropTypes.func,
    removeProject: React.PropTypes.bool,
};

ProjectsRow.defaultProps = {
    current: false,
    removeProject: true,
    setCurrent: null
};

export default ProjectsRow;
