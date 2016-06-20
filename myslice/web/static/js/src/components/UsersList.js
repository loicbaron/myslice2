import React from 'react';
import store from '../stores/UsersStore';
import actions from '../actions/UsersActions';

import List from './base/List';

import UsersRow from'./UsersRow';

//import UsersRow from'./UsersRow';

class UsersList extends React.Component {

    constructor(props) {
        super(props);
        this.state = store.getState();
        this.onChange = this.onChange.bind(this);
    }

    componentDidMount() {
        store.listen(this.onChange);
        actions.fetchUsers();
    }

    componentWillUnmount() {
        store.unlisten(this.onChange);
    }

    onChange(state) {
        this.setState(state);
    }
    
    render() {
        let users = this.state.users;

        if (this.state.errorMessage) {
            return (
                <div>Something is wrong</div>
            );
        }

        return (
            <List>
            {
                users.map(function(user) {
                    return <UsersRow key={user.id} user={user}></UsersRow>;
                    //return <div>{user.id}</div>
                })
            }
            </List>
        );
    }
}

export default UsersList;
