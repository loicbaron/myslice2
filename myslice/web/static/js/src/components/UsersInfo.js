import React from 'react';

import Avatar from 'react-avatar';

import List from './base/List';
import Title from './base/Title';
import AuthoritiesList from'./AuthoritiesList';
import ProjectsList from'./ProjectsList';

class UsersInfo extends React.Component {

    render() {
        var p = this.props.selected;
        console.log(p);
        let name = [p.first_name, p.last_name].join(' ');
        var projectsElement;
        if(p.projects){
            projectsElement = <div><Title title="Projects" /><ProjectsList projects={p.projects} /></div>
        }
        var authorityElement;
        if(p.authority){
            var a = [];
            a.push(p.authority);
            authorityElement = <div><Title title="Authority" subtitle="" /><AuthoritiesList authorities={a} /></div>
        }

        var authoritiesElement;
        if(p.pi_authorities){
            authoritiesElement = <div><Title title="Authorities" subtitle="Manager" /><AuthoritiesList authorities={p.pi_authorities} /></div>
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
