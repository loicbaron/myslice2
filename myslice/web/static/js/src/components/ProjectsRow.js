import React from 'react';

import Element from './base/Element';
import ElementTitle from './base/ElementTitle';
import ElementId from './base/ElementId';
import ElementStatus from './base/ElementStatus';
import ElementIcon from './base/ElementIcon';
import DateTime from './base/DateTime';

class ProjectsRow extends React.Component {

    constructor(props) {
        super(props);
    }


    render() {
        var label = this.props.project.name || this.props.project.shortname;
        var authority = this.props.project.authority_details.name || this.props.project.authority_details.shortname;

        return (
             <Element element={this.props.project} type="project" selected={this.props.selected} selectElement={this.props.selectProject}>
                 <ElementStatus status={this.props.project.status} />
                 <ElementIcon icon="project" />
                 <ElementTitle label={label} detail={this.props.project.shortname} />
                 <ElementId id={this.props.project.id} />
                 <div className="elementDetail">
                     <span className="elementLabel">Users</span> {this.props.project.pi_users.length}
                     &nbsp;&nbsp;&nbsp;&nbsp;
                     <span className="elementLabel">Slices</span> {this.props.project.slices.length}
                     <br />
                     <span className="elementLabel">Managed by</span> {authority}
                 </div>
                 <div className="row elementDate">
                     <div className="col-sm-3">
                         <span className="elementLabel">Created</span>
                         <br />
                         <DateTime timestamp={this.props.project.created} />
                     </div>
                     <div className="col-sm-3">
                         <span className="elementLabel">Enabled</span>
                         <br />
                         <DateTime timestamp={this.props.project.enabled} />
                     </div>
                     <div className="col-sm-3">
                         <span className="elementLabel">Updated</span>
                         <br />
                         <DateTime timestamp={this.props.project.updated} />
                     </div>
                 </div>
             </Element>
         );
    }
 }

export default ProjectsRow;