import React from 'react';

import List from './base/List';
import AuthoritiesRow from'./AuthoritiesRow';

class AuthoritiesList extends React.Component {

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
                                return <AuthoritiesRow key={authority.id} authority={authority} setCurrent={this.props.setCurrent} current={this.props.current} revoke={true} />;
                            }else if(this.props.grant && !containsObject(authority, this.props.rights)){
                                // Grant
                                return <AuthoritiesRow key={authority.id} authority={authority} setCurrent={this.props.setCurrent} current={this.props.current} grant={true} />;
                            }
                        }
                        return <AuthoritiesRow key={authority.id} authority={authority} setCurrent={this.props.setCurrent} current={this.props.current} />;
                    }.bind(this))
                }
                </List>
            );
        }

    }
}

AuthoritiesList.propTypes = {
    authorities: React.PropTypes.array.isRequired,
    current: React.PropTypes.object,
    setCurrent: React.PropTypes.func,
    grant: React.PropTypes.bool,
    revoke: React.PropTypes.bool,
};

AuthoritiesList.defaultProps = {
    current: null,
    setCurrent: null,
    grant: false,
    revoke: false,
};

export default AuthoritiesList;
