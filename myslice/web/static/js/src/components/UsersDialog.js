import React from 'react';

import actions from '../actions/UsersActions';
import store from '../stores/UsersStore';

import Dialog from './base/Dialog';
import DialogPanel from './base/DialogPanel';
import DialogHeader from './base/DialogHeader';
import DialogBody from './base/DialogBody';
import Title from './base/Title';
import UsersList from './UsersList';

class UsersDialog extends React.Component {

    constructor(props) {
        super(props);
        this.state = store.getState();
        this.onChange = this.onChange.bind(this);
    }

    componentDidMount() {
        store.listen(this.onChange);
        this.fetchUsers();
    }

    componentWillUnmount() {
        store.unlisten(this.onChange);
    }

    onChange(state) {
        this.setState(state);
    }

    /* fetch the users list */
    fetchUsers() {
        actions.fetchUsers();
    }

    render() {
        return (
            <Dialog close={this.props.close}>
                <DialogPanel>
                    <DialogHeader>
                        <Title title="Add Users" />
                    </DialogHeader>
                    <DialogBody>
                        <UsersList users={this.state.users} />
                    </DialogBody>
                </DialogPanel>
            </Dialog>
        );
    }
}

UsersDialog.propTypes = {
    close: React.PropTypes.func
};

UsersDialog.defaultProps = {
    close: null
};

export default UsersDialog;
