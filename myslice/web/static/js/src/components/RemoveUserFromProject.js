import React from 'react';

import store from '../stores/ProjectsStore';
import actions from '../actions/ProjectsActions';

class RemoveUserFromProject extends React.Component {
    constructor(props) {
        super(props);
        this.state = store.getState();
        this.onChange = this.onChange.bind(this);
        this.removeUser = this.removeUser.bind(this);

    }
    onChange(state) {
        this.setState(state);
    }
    componentDidMount() {
        store.listen(this.onChange);
    }

    componentWillUnmount() {
        store.unlisten(this.onChange);
    }
    removeUser(){
        actions.removeUser(this.props.user);
    }
    render() {
        var containsUser = function(user, list){
            for(var i=0; i<list.length; i++){            
                if(list[i].id==user.id){
                    return true;
                }
            }
            return false;
        };
        if(this.state.removeUserFromProject==this.props.user){
            return(
                <div className="elementButton">
                    <i className="fa fa-lg fa-cog fa-spin" />
                </div>
            );
        }else if(containsUser(this.props.user, this.state.removedUsers[this.state.current.project.id])){
            return(
                <div className="elementButton bg-danger">
                    <span className="text-danger"> Removed </span>
                </div>
            );
        }else{
            return(
                <div className="elementButton">
                    <button type="button" onClick={this.removeUser} >
                    <i className="fa fa-ban" aria-hidden="true"></i>
                    &nbsp;
                    Remove user
                    </button>
                </div>
            );
        }
    }
 }

RemoveUserFromProject.propTypes = {
    user: React.PropTypes.object.isRequired,
};

export default RemoveUserFromProject;
