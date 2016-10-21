import React from 'react';
import Avatar from 'react-avatar';

import Element from './base/Element';
import ElementTitle from './base/ElementTitle';
import ElementId from './base/ElementId';
import ElementStatus from './base/ElementStatus';
import ElementIcon from './base/ElementIcon';
import DateTime from './base/DateTime';

import AddUserToProject from './AddUserToProject';
import RemoveUserFromProject from './RemoveUserFromProject';

class UsersRow extends React.Component {
    constructor(props) {
        super(props);
    }
    render() {
        var authority = this.props.user.authority.name || this.props.user.authority.shortname;

        var num_slices = 0;
        if (this.props.user.hasOwnProperty('slices')) {
            num_slices = this.props.user.slices.length
        }

        var num_projects = 0;
        if (this.props.user.hasOwnProperty('projects')) {
            num_projects = this.props.user.projects.length
        }
        var button = '';
        if(this.props.addUser){
            button = <AddUserToProject user={this.props.user} />
        }
        if(this.props.removeUser){
            button = <RemoveUserFromProject user={this.props.user} />
        }

        var fullname = [this.props.user.first_name, this.props.user.last_name].join(' ');
        if (!fullname) {
            fullname = this.props.user.shortname;
        }
        return (
             <Element element={this.props.user} type="user" setCurrent={this.props.setCurrent} current={this.props.current}>
                 <ElementStatus status={this.props.user.status} />
                 <Avatar className="elementIcon" email={this.props.user.email} name={fullname} round={true} size={40} color="#CFE2F3" />
                 <ElementTitle label={fullname} detail={this.props.user.email} />
                 <ElementId id={this.props.user.id} />
                 {button}
                 <div className="elementDetail">
                     <span className="elementLabel">Projects</span> {num_projects}
                     &nbsp;&nbsp;&nbsp;&nbsp;
                     <span className="elementLabel">Slices</span> {num_slices}
                     <br />
                     <span className="elementLabel">Part of</span> {authority}
                 </div>
             </Element>
         );
    }
 }

UsersRow.propTypes = {
    user: React.PropTypes.object.isRequired,
    addUser: React.PropTypes.bool,
    removeUser: React.PropTypes.bool,
    current: React.PropTypes.object,
    setCurrent: React.PropTypes.func,
};

UsersRow.defaultProps = {
    current: false,
    addUser: false,
    removeUser: false,
};

export default UsersRow;
