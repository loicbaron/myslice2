import React from 'react';

import List from './base/List';
import UsersRow from'./UsersRow';

class UsersList extends React.Component {
    
    render() {
        return (
            <List>
            {
                this.props.users.map(function(user) {
                    return <UsersRow key={user.id} user={user} selected={this.props.selected} selectUser={this.props.selectUser} />;
                }.bind(this))
            }
            </List>
        );
    }
}

UsersList.defaultProps = {
    'filter' : {
        'type' : null,
        'value' : null
    }

};

export default UsersList;
