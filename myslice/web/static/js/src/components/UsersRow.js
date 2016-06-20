import React from 'react';

import Element from './base/Element';
import ElementTitle from './base/ElementTitle';
import ElementId from './base/ElementId';
import ElementStatus from './base/ElementStatus';
import ElementIcon from './base/ElementIcon';
import DateTime from './base/DateTime';

class UsersRow extends React.Component {

    render() {
        var label = this.props.user.first_name +' '+ this.props.user.last_name;
        var authority = this.props.user.authority;

        return (
             <Element element={this.props.user} type="user" select={this.props.select}>
                 <ElementStatus status={this.props.user.status} />
                 <ElementIcon icon="user" />
                 <ElementTitle label={label} detail={this.props.user.email} />
                 <ElementId id={this.props.user.id} />
                 <div className="elementDetail">
                     <span className="elementLabel">Projects</span> {this.props.user.projects.length}
                     &nbsp;&nbsp;&nbsp;&nbsp;
                     <span className="elementLabel">Slices</span> {this.props.user.slices.length}
                     <br />
                     <span className="elementLabel">Managed by</span> {authority}
                 </div>
                 <div className="row elementDate">
                     <div className="col-sm-3">
                         <span className="elementLabel">Created</span>
                         <br />
                         <DateTime timestamp={this.props.user.created} />
                     </div>
                     <div className="col-sm-3">
                         <span className="elementLabel">Enabled</span>
                         <br />
                         <DateTime timestamp={this.props.user.enabled} />
                     </div>
                     <div className="col-sm-3">
                         <span className="elementLabel">Updated</span>
                         <br />
                         <DateTime timestamp={this.props.user.updated} />
                     </div>
                 </div>
             </Element>
         );
    }
 }

UsersRow.propTypes = {
    user: React.PropTypes.object.isRequired,
    select: React.PropTypes.bool
};

UsersRow.defaultProps = {
    select: false
};

export default UsersRow;
