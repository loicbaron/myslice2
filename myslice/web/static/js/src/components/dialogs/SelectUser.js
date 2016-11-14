import React from 'react';

import actions from '../../actions/dialogs/SelectUser';
import store from '../../stores/dialogs/SelectUser';

import { DialogPanel, Dialog, DialogBody, DialogHeader, DialogBar, DialogFooter } from '../base/Dialog';
import Title from '../base/Title';
import { UserList } from '../objects/User';

import SelectAuthority from '../forms/SelectAuthority';
import UsersFilter from '../UsersFilter';

class SelectUserDialog extends React.Component {

    constructor(props) {
        super(props);
        this.state = store.getState();
        this.onChange = this.onChange.bind(this);
        this.handleFilter = this.handleFilter.bind(this);
    }

    componentDidMount() {
        store.listen(this.onChange);

        this.fetchUsers();

        // if (this.props.exclude.length > 0) {
        //     actions.updateExcludeUsers(this.props.exclude);
        // }
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

    cancel() {

    }

    apply() {

    }

    render() {
        // if (Object.keys(this.state.filter).length>0){
        //     var usersList = <UserList users={this.state.filteredUsers} addUser={this.props.addUser} />
        // } else {
        //     var usersList = <UserList users={this.state.users} />
        // }

        return (
            <Dialog close={this.props.close}>
                <DialogPanel>
                    <DialogHeader>
                        <Title title="Add Users" />
                    </DialogHeader>
                    <DialogBar>
                        <SelectAuthority placeholder="Filter by Organization" value={this.state.authority.id} handleChange="" />
                        <UsersFilter handleChange={this.handleFilter} users={this.state.users} />
                    </DialogBar>
                    <DialogBody>
                        <UserList users={this.state.users} />
                    </DialogBody>
                    <DialogFooter>
                        <button className="cancel" onClick={this.cancel} >
                            Cancel
                        </button>
                        <button className="apply" onClick={this.apply} >
                            Apply
                        </button>
                    </DialogFooter>
                </DialogPanel>
            </Dialog>
        );
    }
}

SelectUserDialog.propTypes = {
    close: React.PropTypes.func,
    addUser: React.PropTypes.bool,
};

SelectUserDialog.defaultProps = {
    close: null,
    addUser: false,
};

export default SelectUserDialog;
