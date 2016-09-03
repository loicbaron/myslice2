import React from 'react';

import store from '../stores/ProjectsStore';
import actions from '../actions/ProjectsActions';

class DeleteProject extends React.Component {
    constructor(props) {
        super(props);
        this.state = store.getState();
        this.onChange = this.onChange.bind(this);
        this.deleteProject = this.deleteProject.bind(this);

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
    deleteProject(){
        actions.deleteProject(this.props.project);
    }
    render() {
        var containsObject = function(obj, list){
            for(var i=0; i<list.length; i++){            
                if(list[i].id==obj.id){
                    return true;
                }
            }
            return false;
        };
        if(this.state.deleteProj==this.props.project){
            return(
                <div className="elementButton">
                    <i className="fa fa-lg fa-cog fa-spin" />
                </div>
            );
        }else if(this.state.deletedProjects.indexOf(this.props.project)>-1){
            return(
                <div className="elementButton bg-danger">
                    <span className="text-danger"> Deleted </span>
                </div>
            );
        }else{
            return(
                <div className="elementButton">
                    <button type="button" onClick={this.deleteProject} >
                    <i className="fa fa-trash" aria-hidden="true"></i>
                    &nbsp;
                    Delete
                    </button>
                </div>
            );
        }
    }
 }

DeleteProject.propTypes = {
    project: React.PropTypes.object.isRequired,
};

export default DeleteProject;
