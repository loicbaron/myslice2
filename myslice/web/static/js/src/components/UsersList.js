import React from 'react';

import store from '../stores/UsersStore';
import actions from '../actions/UsersActions';

import List from './base/List';
import UsersRow from'./UsersRow';

class UsersList extends React.Component {

    constructor(props) {
        super(props);
        this.state = store.getState();
        this.onChange = this.onChange.bind(this);
    }

    componentDidMount() {
        store.listen(this.onChange);

        this.fetchUsers({
            belongTo: this.props.belongTo
        });

    }

    componentWillReceiveProps(nextProps) {
        this.fetchUsers({
            belongTo: nextProps.belongTo
        });
    }

    componentWillUnmount() {
        store.unlisten(this.onChange);
    }

    onChange(state) {
        this.setState(state);
    }

    fetchUsers(options) {
        actions.fetchUsers({
            belongTo: options.belongTo
        });
    }

    render() {

        return (
            <List>
            {
                this.state.users.map(function(user) {
                    return <UsersRow key={user.id} user={user} select={this.props.select} />;
                }.bind(this))
            }
            </List>
        );
    }
}

UsersList.propTypes = {
    belongTo: React.PropTypes.object,
    select: React.PropTypes.bool
};

UsersList.defaultProps = {
    belongTo: { type: null, id: null},
    select: false
};

export default UsersList;
