import React from 'react';

import List from './base/List';
import UsersRow from'./UsersRow';

class UsersList extends React.Component {

    render() {
        return (
            <List>
            {
                this.props.users.map(function(user) {
                    return <UsersRow key={user.id} user={user} setCurrent={this.props.setCurrent} current={this.props.current} />;
                }.bind(this))
            }
            </List>
        );
    }
}

UsersList.propTypes = {
    users: React.PropTypes.array.isRequired,
    current: React.PropTypes.object,
    setCurrent: React.PropTypes.func
};

UsersList.defaultProps = {
    current: null,
    setCurrent: null
};

export default UsersList;
