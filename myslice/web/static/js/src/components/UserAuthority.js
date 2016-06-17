import React from 'react';
import store from '../stores/UserProfileStore';
import actions from '../actions/UserProfileActions';

export default class UserAuthority extends React.Component {

    constructor(props) {
        super(props);
        this.state = store.getState();
        this.onChange = this.onChange.bind(this);
    }

    componentDidMount() {
        store.listen(this.onChange);
        actions.fetchProfile();
    }

    componentWillUnmount() {
        store.unlisten(this.onChange);
    }
    
    // listen to the Store once something changes
    onChange(state) {
        this.setState(state);
        if(this.state.authority!=''){
            console.log('UserAuthority: '+this.state.authority);
            this.props.handleUpdateAuthority.call(this, this.state.authority);
        }
    }

    render() {

        return (
            <input  value={this.state.authority} name="authority" 
                    type="text" />
            )
    }


}
