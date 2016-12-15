import React from 'react';

import Avatar from 'react-avatar';

import Title from './base/Title';
import { AuthorityList } from'./objects/Authority';
import { ProjectList } from'./objects/Project';

class UsersInfo extends React.Component {

/*

TODO

Buttons:

Authority = Grant/Revoke manager rights
Manager = Revoke rights
Project = Remove from Project

Has a private/pub keys: True/False
- Download pub key
- Generate new keys

Later:
- Statistics

*/

    render() {
        var u = this.props.element;
        if(u.hasOwnProperty('first_name') && u.hasOwnProperty('last_name')){
            let name = [u.first_name, u.last_name].join(' ');
        }else{
            let name = u.shortname;
        }
        var projectsElement;
        if(u.projects){
            projectsElement = <div><Title title="Projects" /><ProjectList projects={u.projects} /></div>
        }
        var authorityElement;
        if(u.authority){
            var a = [];
            a.push(u.authority);
            authorityElement = <div><Title title="Authority" subtitle="" /><AuthorityList authorities={a} grant={true} revoke={false} rights={u.pi_authorities} /></div>
        }

        var authoritiesElement;
        if(u.pi_authorities){
            authoritiesElement = <div><Title title="Manager" subtitle="" /><AuthorityList authorities={u.pi_authorities} grant={false} revoke={true} rights={u.pi_authorities} /></div>
        }
        return (
        <div>
            <div className = "row">
                <div className="col-sm-2 vcenter settings-group profileAvatar">
                <Avatar className="avatar" email={u.email} name={name} round={true} />
                </div>
                <div className="col-sm-8 vcenter">{u.email}</div>
            </div>
            {authorityElement}
            {authoritiesElement}
            {projectsElement}
        </div>
        );
    }
}

export default UsersInfo;
