import React from 'react';

import Element from './base/Element';
import ElementTitle from './base/ElementTitle';
import ElementId from './base/ElementId';
import ElementStatus from './base/ElementStatus';
import ElementIcon from './base/ElementIcon';
import DateTime from './base/DateTime';

import DeleteProject from './DeleteProject';

class AuthoritiesRow extends React.Component {

    render() {
        var label = this.props.authority.name || this.props.authority.shortname;
        var users;
        if(this.props.authority.users){
            users = <span className="elementLabel">Users {this.props.authority.users.length} </span>
        }
        var pi_users;
        if(this.props.authority.pi_users){
            pi_users = <span className="elementLabel">Managers {this.props.authority.pi_users.length} </span>
        }
        var projects;
        if(this.props.authority.projects){
            projects = <span className="elementLabel">Slices {this.props.authority.projects.length}</span>
        }
        var created;
        if(this.props.authority.created){
            created = <div className="col-sm-3"><DateTime label="Created" timestamp={this.props.authority.created}/></div>
        }
        var enabled;
        if(this.props.authority.enabled){
            enabled = <div className="col-sm-3"><DateTime label="Enabled" timestamp={this.props.authority.enabled}/></div>
        }
        var updated;
        if(this.props.authority.updated){
            updated = <div className="col-sm-3"><DateTime label="Updated" timestamp={this.props.authority.updated}/></div>
        }
        var authorityElement;
        if(this.props.authority.authority){
            var authority = this.props.authority.authority.name || this.props.authority.authority.shortname;
            authorityElement = <span className="elementLabel">Managed by {authority}</span>
        }
        var authorityDetails;
        if(users || projects || pi_users || authorityElement){
            authorityDetails = <div className="elementDetail">{users}&nbsp;&nbsp;{projects}&nbsp;&nbsp;{pi_users}<br/>{authorityElement}</div>
        }
        return (
            <Element element={this.props.authority} type="authority" setCurrent={this.props.setCurrent} current={this.props.current}>
                <ElementIcon icon="authority"/>
                <ElementTitle label={label} detail={this.props.authority.shortname}/>
                <ElementId id={this.props.authority.id}/>
                {authorityDetails}
                <div className="row elementDate">
                    {created}
                    {enabled}
                    {updated}
                </div>
            </Element>
        );
    }
}

AuthoritiesRow.propTypes = {
    authority: React.PropTypes.object.isRequired,
    current: React.PropTypes.object,
    setCurrent: React.PropTypes.func,
    removeProject: React.PropTypes.bool,
};

AuthoritiesRow.defaultProps = {
    current: false,
    removeProject: true,
    setCurrent: null
};

export default AuthoritiesRow;
