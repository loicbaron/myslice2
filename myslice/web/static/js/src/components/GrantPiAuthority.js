import React from 'react';

import store from '../stores/UsersStore';
import actions from '../actions/UsersActions';

import common from '../utils/Commons';

class GrantPiAuthority extends React.Component {
    constructor(props) {
        super(props);
        this.state = store.getState();
        this.onChange = this.onChange.bind(this);
        this.grantPiRights = this.grantPiRights.bind(this);

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
    grantPiRights(){
        actions.grantPiRights(this.props.authority);
    }
    render() {
        console.log("render grant "+this.props.authority.id);
        console.log(this.props.authority);
        var style;
        if(this.props.topPosition){
            style=this.props.topPosition;
        }
        if(this.state.grantPiAuthority==this.props.authority.id){
            return(
                <div className="elementButton" style={style}>
                    <i className="fa fa-lg fa-cog fa-spin" />
                </div>
            );
        }else if(common.containsObject(this.props.authority, this.state.grantedAuthorities[this.state.current.user.id])){
            return(
                <div className="elementButton bg-success" style={style}>
                    <span className="success"> Granted </span>
                </div>
            );
        }else{
            return(
                <div className="elementButton" style={style}>
                    <button type="button" onClick={this.grantPiRights} >
                        <i className="fa fa-thumbs-o-up" aria-hidden="true"></i>
                        &nbsp;
                        Grant rights
                    </button>
                </div>
            );
        }
    }
 }

GrantPiAuthority.propTypes = {
    authority: React.PropTypes.object.isRequired,
};

export default GrantPiAuthority;
