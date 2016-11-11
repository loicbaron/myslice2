import React from 'react';

import { List, ListSimple } from '../base/List';
import { Element } from '../base/Element';
import ElementTitle from '../base/ElementTitle';
import ElementId from '../base/ElementId';
import DateTime from '../base/DateTime';

import GrantPiAuthority from '../GrantPiAuthority';
import RevokePiAuthority from '../RevokePiAuthority';

class AuthorityElement extends React.Component {

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
        var button;
        var minHeight = {'minHeight':'100px'};
        var topPosition = {'top':'25px'};
        if(this.props.revoke){
            button = <RevokePiAuthority authority={this.props.authority} topPosition={topPosition} />
        }
        if(this.props.grant){
            button = <GrantPiAuthority authority={this.props.authority} topPosition={topPosition} />
        }
        return (
            <Element element={this.props.authority}
                     type="authority"
                     setCurrent={this.props.setCurrent}
                     current={this.props.current}
                     icon="authority"
            >
                <ElementTitle label={label} detail={this.props.authority.shortname}/>
                <ElementId id={this.props.authority.id}/>
                {button}
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

AuthorityElement.propTypes = {
    authority: React.PropTypes.object.isRequired,
    current: React.PropTypes.object,
    setCurrent: React.PropTypes.func,
    revoke: React.PropTypes.bool,
    grant: React.PropTypes.bool,
};

AuthorityElement.defaultProps = {
    revoke: false,
    grant: false,
    current: false,
    setCurrent: null
};


class AuthorityList extends React.Component {

    render() {
        var containsObject = function(obj, list){
            for(var i=0; i<list.length; i++){
                if(list[i].id==obj.id){
                    return true;
                }
            }
            return false;
        };

        if (!this.props.authorities || this.props.authorities.length==0) {
            return <List>No authority</List>
        } else {
            return (
                <List>
                {
                    this.props.authorities.map(function(authority) {
                        if((this.props.grant || this.props.revoke) && this.props.rights){
                            if(this.props.revoke && containsObject(authority, this.props.rights)){
                                // Revoke button
                                return <AuthorityElement key={authority.id} authority={authority} setCurrent={this.props.setCurrent} current={this.props.current} revoke={true} />;
                            }else if(this.props.grant && !containsObject(authority, this.props.rights)){
                                // Grant
                                return <AuthorityElement key={authority.id} authority={authority} setCurrent={this.props.setCurrent} current={this.props.current} grant={true} />;
                            }
                        }
                        return <AuthorityElement key={authority.id} authority={authority} setCurrent={this.props.setCurrent} current={this.props.current} />;
                    }.bind(this))
                }
                </List>
            );
        }

    }
}

AuthorityList.propTypes = {
    authorities: React.PropTypes.array.isRequired,
    current: React.PropTypes.object,
    setCurrent: React.PropTypes.func,
    grant: React.PropTypes.bool,
    revoke: React.PropTypes.bool,
};

AuthorityList.defaultProps = {
    current: null,
    setCurrent: null,
    grant: false,
    revoke: false,
};

export { AuthorityElement, AuthorityList };
