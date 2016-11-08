import React from 'react';
import Avatar from 'react-avatar';

import List from '../base/List';
import Element from '../base/Element';
import ElementTitle from '../base/ElementTitle';
import ElementId from '../base/ElementId';
import DateTime from '../base/DateTime';

import AddUserToProject from '../AddUserToProject';
import RemoveUserFromProject from '../RemoveUserFromProject';

class UserElement extends React.Component {
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
             <Element element={this.props.user}
                      type="user"
                      setCurrent={this.props.setCurrent}
                      current={this.props.current}
                      status={this.props.user.status}
             >
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

UserElement.propTypes = {
    user: React.PropTypes.object.isRequired,
    addUser: React.PropTypes.bool,
    removeUser: React.PropTypes.bool,
    current: React.PropTypes.object,
    setCurrent: React.PropTypes.func,
};

UserElement.defaultProps = {
    current: false,
    addUser: false,
    removeUser: false,
};


class UserList extends React.Component {

    render() {
        return (
            <div>
                <List>
                {
                    this.props.users.map(function(user) {
                        return <UserElement key={user.id} user={user} setCurrent={this.props.setCurrent} current={this.props.current} addUser={this.props.addUser} removeUser={this.props.removeUser} />;
                    }.bind(this))
                }
                </List>
            </div>
        );
    }
}

UserList.propTypes = {
    users: React.PropTypes.array.isRequired,
    current: React.PropTypes.object,
    addUser: React.PropTypes.bool,
    removeUser: React.PropTypes.bool,
    setCurrent: React.PropTypes.func
};

UserList.defaultProps = {
    current: null,
    setCurrent: null,
    addUser: false,
    removeUser: false,
};


export { UserElement, UserList };
