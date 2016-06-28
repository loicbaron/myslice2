import React from 'react';

import Element from './base/Element';
import ElementTitle from './base/ElementTitle';
import ElementId from './base/ElementId';
import ElementStatus from './base/ElementStatus';
import ElementIcon from './base/ElementIcon';
import DateTime from './base/DateTime';

class UsersRow extends React.Component {
    constructor(props) {
        super(props);
        this.addUser = this.addUser.bind(this);
        this.state = {'loading':false}
    }
    addUser(value){
        this.setState({'loading':true});
        this.props.addUser(this.props.user);
    }

    render() {
        var authority = this.props.user.authority.name || this.props.user.authority.shortname;

        var label = '';
        if (this.props.user.hasOwnProperty('first_name')) {
            label += this.props.user.first_name + ' ';
        }
        if (this.props.user.hasOwnProperty('last_name')) {
            label += this.props.user.last_name;
        }
        if (!label) {
            label = this.props.user.shortname;
        }

        var num_slices = 0;
        if (this.props.user.hasOwnProperty('slices')) {
            num_slices = this.props.user.slices.length
        }

        var num_projects = 0;
        if (this.props.user.hasOwnProperty('projects')) {
            num_projects = this.props.user.projects.length
        }
        var addButton = '';
        if(this.props.addUser){
            if(this.state.loading){
                addButton = <div className="elementButton"><i className="fa fa-lg fa-cog fa-spin" /></div>
            }else{
                addButton = <div className="elementButton"><button type="button" onClick={this.addUser} >Add user</button></div>
            }
        }

        return (
             <Element element={this.props.user} type="user" select={this.props.select}>
                 <ElementStatus status={this.props.user.status} />
                 <ElementIcon icon="user" />
                 <ElementTitle label={label} detail={this.props.user.email} />
                 <ElementId id={this.props.user.id} />
                 {addButton}
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
    addUser: React.PropTypes.func,
    select: React.PropTypes.bool
};

UsersRow.defaultProps = {
    select: false
};

export default UsersRow;
