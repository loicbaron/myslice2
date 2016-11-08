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
        var p = this.props.selected;
        let name = [p.first_name, p.last_name].join(' ');
        var projectsElement;
        if(p.projects){
            projectsElement = <div><Title title="Projects" /><ProjectList projects={p.projects} /></div>
        }
        var authorityElement;
        if(p.authority){
            var a = [];
            a.push(p.authority);
            console.log("UsersInfo p.authority");
            console.log(p.authority);
            console.log(p.pi_authorities);
            authorityElement = <div><Title title="Authority" subtitle="" /><AuthorityList authorities={a} grant={true} revoke={false} rights={p.pi_authorities} /></div>
        }

        var authoritiesElement;
        if(p.pi_authorities){
            console.log("UsersInfo pi_authorities");
            console.log(p.pi_authorities);
            authoritiesElement = <div><Title title="Manager" subtitle="" /><AuthorityList authorities={p.pi_authorities} grant={false} revoke={true} rights={p.pi_authorities} /></div>
        }
        return (
        <div>
            <div className = "row">
                <div className="col-sm-2 vcenter settings-group profileAvatar">
                <Avatar className="avatar" email={p.email} name={name} round={true} />
                </div>
                <div className="col-sm-8 vcenter">{p.email}</div>
            </div>
            {authorityElement}
            {authoritiesElement}
            {projectsElement}
        </div>
        );
    }
}

export default UsersInfo;
