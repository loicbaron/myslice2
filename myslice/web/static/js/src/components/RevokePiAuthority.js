import React from 'react';

import store from '../stores/UsersStore';
import actions from '../actions/UsersActions';

import common from '../utils/Commons';

class RevokePiAuthority extends React.Component {
    constructor(props) {
        super(props);
        this.state = store.getState();
        this.onChange = this.onChange.bind(this);
        this.revokePiRights = this.revokePiRights.bind(this);

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
    revokePiRights(){
        actions.revokePiRights(this.props.authority);
    }
    render() {
        var style;
        if(this.props.topPosition){
            style=this.props.topPosition;
        }
        console.log("render revoke "+this.props.authority.id);
        console.log(this.props.authority);
        if(this.state.revokePiAuthority==this.props.authority.id){
            return(
                <div className="elementButton" style={style}>
                    <i className="fa fa-lg fa-cog fa-spin" />
                </div>
            );
        }else if(this.state.current.user.id in Object.keys(this.state.revokedAuthorities) && common.containsObject(this.props.authority, this.state.revokedAuthorities[this.state.current.user.id])){
            return(
                <div className="elementButton bg-danger" style={style}>
                    <span className="text-danger"> Removed </span>
                </div>
            );
        }else{
            return(
                <div className="elementButton" style={style}>
                    <button type="button" onClick={this.revokePiRights} >
                    <i className="fa fa-thumbs-o-down" aria-hidden="true"></i>
                    &nbsp;
                    Revoke rights
                    </button>
                </div>
            );
        }
    }
 }

RevokePiAuthority.propTypes = {
    authority: React.PropTypes.object.isRequired,
};

export default RevokePiAuthority;
