import React from 'react';
import moment from 'moment';

import Element from './base/Element';
import ElementTitle from './base/ElementTitle';
import ElementId from './base/ElementId';
import ElementStatus from './base/ElementStatus';
import DateTime from './base/DateTime';

class ProjectLabel extends React.Component {

    label() {
        let label = '';
        switch(this.props.project.action) {
            case 'REQ':
                label = 'requested ' + this.props.project.object.type;
        }
        return label;
    }

    render() {
        return (

            <div className="row">
                <div className="col-md-12">
                    <div className="elementIcon">
                <img src="/static/icons/projects-w-24.png" alt="" />
            </div>
                    <div className="elementLabel">{ this.label() }</div>
                </div>
            </div>
        )
    }
}

class ProjectStatus extends React.Component {

    render() {
        return (
            <div className="row">
                <div className="col-md-12">
                    <div className="elementStatus">{ this.props.status }</div>
                </div>
            </div>
        )
    }
}


class ProjectsRow extends React.Component {

    constructor(props) {
        super(props);
    }


    render() {
        var label = this.props.project.name || this.props.project.shortname;
        var authority = this.props.project.authority_details.name || this.props.project.authority_details.shortname;

        return (
             <Element element={this.props.project}>
                 <ElementTitle label={label} detail={this.props.project.shortname} />
                 <ElementId id={this.props.project.id} />
                 <div className="elementDetail">
                     <span className="elementLabel">Users</span> {this.props.project.pi_users.length}
                     &nbsp;&nbsp;&nbsp;&nbsp;
                     <span className="elementLabel">Slices</span> {this.props.project.slices.length}
                     <br />
                     <span className="elementLabel">Managed by</span> {authority}
                 </div>
                 <div className="elementDate">
                     <span className="elementLabel">Created</span> <DateTime timestamp={this.props.project.created} />
                     <br />
                     <span className="elementLabel">Enabled</span> <DateTime timestamp={this.props.project.enabled} />
                     <br />
                     <span className="elementLabel">Updated</span> <DateTime timestamp={this.props.project.updated} />
                 </div>
                 <ElementStatus status={this.props.project.status} />
             </Element>
         );
    }
 }

export default ProjectsRow;