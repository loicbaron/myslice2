import React from 'react';

import actions from '../actions/UsersActions';
import store from '../stores/UsersStore';

import { DialogPanel, Dialog, DialogBody, DialogHeader, DialogFooter } from './base/Dialog';
import Title from './base/Title';
import { UserList } from './objects/User';
import UsersFilter from './UsersFilter';

class UsersDialog extends React.Component {

    constructor(props) {
        super(props);
        this.state = store.getState();
        this.onChange = this.onChange.bind(this);
        this.handleFilter = this.handleFilter.bind(this);
    }

    componentDidMount() {
        store.listen(this.onChange);
        this.fetchUsers();
        if(this.props.exclude.length>0){
            actions.updateExcludeUsers(this.props.exclude);
        }
    }

    componentWillUnmount() {
        store.unlisten(this.onChange);
    }

    onChange(state) {
        this.setState(state);
    }
    handleFilter(value) {
        var f = {'email':value,'shortname':value}
        actions.updateFilter(f);
        actions.updateFilteredUsers();
    }
    /* fetch the users list */
    fetchUsers(filter={}) {
        switch (this.props.from){
            case 'authority':
                actions.fetchFromAuthority(filter);
                break;
            default:
                actions.fetchUsers(filter);
        }
    }

    render() {
        if(Object.keys(this.state.filter).length>0){
            var usersList = <UserList users={this.state.filteredUsers} addUser={this.props.addUser} />
        }else{
            var usersList = <UserList users={this.state.users} addUser={this.props.addUser} />
        }

        return (
            <Dialog close={this.props.close}>
                <DialogPanel>
                    <DialogHeader>
                        <Title title="Add Users" />
                    </DialogHeader>
                    <DialogBody>
                        <UsersFilter handleChange={this.handleFilter} users={this.state.users} />
                        {usersList}
                    </DialogBody>
                </DialogPanel>
            </Dialog>
        );
    }
}

UsersDialog.propTypes = {
    close: React.PropTypes.func,
    addUser: React.PropTypes.bool,
};

UsersDialog.defaultProps = {
    close: null,
    addUser: false,
};

export default UsersDialog;
