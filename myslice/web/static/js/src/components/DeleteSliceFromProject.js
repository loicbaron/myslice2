import React from 'react';

import store from '../stores/ProjectsStore';
import actions from '../actions/ProjectsActions';

class DeleteSliceFromProject extends React.Component {
    constructor(props) {
        super(props);
        this.state = store.getState();
        this.onChange = this.onChange.bind(this);
        this.deleteSlice = this.deleteSlice.bind(this);

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
    deleteSlice(){
        actions.deleteSlice(this.props.slice);
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
        if(this.state.deleteSliceFromProject==this.props.slice){
            return(
                <div className="elementButton">
                    <i className="fa fa-lg fa-cog fa-spin" />
                </div>
            );
        }else if(containsObject(this.props.slice, this.state.deletedSlices[this.state.current.project.id])){
            return(
                <div className="elementButton bg-danger">
                    <span className="text-danger"> Deleted </span>
                </div>
            );
        }else{
            return(
                <div className="elementButton">
                    <button type="button" onClick={this.deleteSlice} >
                    <i className="fa fa-trash" aria-hidden="true"></i>
                    &nbsp;
                    Delete
                    </button>
                </div>
            );
        }
    }
 }

DeleteSliceFromProject.propTypes = {
    slice: React.PropTypes.object.isRequired,
};

export default DeleteSliceFromProject;
