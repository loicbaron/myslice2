import React from 'react';

import Element from './base/Element';
import ElementTitle from './base/ElementTitle';
import ElementId from './base/ElementId';
import ElementStatus from './base/ElementStatus';
import ElementIcon from './base/ElementIcon';
import DateTime from './base/DateTime';
import SlicesRow from'./SlicesRow';
import SlicesList from './SlicesList'
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
            slices = <span className="elementLabel">Slices: {this.props.project.slices.length}</span>
        }
        var slicesInDashboard;
        if(this.props.project.slices){
            var slicesInDashboard = <div>
            {
                this.props.project.slices.map(function (slice) {
                    var slice_link="/slices/"+slice.hrn;
                    return <span className="elementLabel"><a href={slice_link}>{slice.shortname}</a></span>;
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
        if (this.props.detailed) {
            return (
                <Element element={this.props.project} type="project" setCurrent={this.props.setCurrent}
                         current={this.props.current} minHeight={minHeight}>
                    <ElementStatus status={this.props.project.status}/>
                    <ElementIcon icon="project"/>
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
                <Element element={this.props.project} type="project" setCurrent={this.props.setCurrent}
                         current={this.props.current} minHeight={minHeight}>
                    <ElementIcon icon="project"/>
                    <a href="/projects"><ElementTitle label={label} detail={this.props.project.shortname} /></a>

                    <ElementId id={this.props.project.id} />

                    <div><i className="fa fa-tasks fa-lg"></i> Slices: {slicesInDashboard}</div>

                </Element>
            );
        }

    }
}

ProjectsRow.propTypes = {
    project: React.PropTypes.object.isRequired,
    current: React.PropTypes.object,
    setCurrent: React.PropTypes.func,
    removeProject: React.PropTypes.bool,
    detailed: React.PropTypes.bool,
};

ProjectsRow.defaultProps = {
    current: false,
    removeProject: true,
    setCurrent: null,
    detailed: true,
};

export default ProjectsRow;
