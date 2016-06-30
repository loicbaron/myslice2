import React from 'react';

import store from '../stores/ProjectsStore';
import actions from '../actions/ProjectsActions';

class AddUserToProject extends React.Component {
    constructor(props) {
        super(props);
        this.state = store.getState();
        this.onChange = this.onChange.bind(this);
        this.addUser = this.addUser.bind(this);

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
    addUser(){
        actions.addUser(this.props.user);
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
        if(this.state.addUserToProject==this.props.user){
            return(
                <div className="elementButton">
                    <i className="fa fa-lg fa-cog fa-spin" />
                </div>
            );
        }else if(containsUser(this.props.user, this.state.current.users)){
            return(
                <div className="elementButton bg-success">
                    <span className="success"> Added </span>
                </div>
            );
        }else{
            return(
                <div className="elementButton">
                    <button type="button" onClick={this.addUser} >Add user</button>
                </div>
            );
        }
    }
 }

AddUserToProject.propTypes = {
    user: React.PropTypes.object.isRequired,
};

export default AddUserToProject;
