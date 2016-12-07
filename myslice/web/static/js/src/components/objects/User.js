import React from 'react';
import Avatar from 'react-avatar';

import { List, ListSimple } from '../base/List';
import { Element } from '../base/Element';
import ElementTitle from '../base/ElementTitle';
import ElementId from '../base/ElementId';
import DateTime from '../base/DateTime';

const UserElement = ({user, isSelected, handleSelect, options}) => {

    let authority = user.authority.name || user.authority.shortname;

    let num_slices = 0;
    if (user.hasOwnProperty('slices')) {
        num_slices = user.slices.length
    }

    let num_projects = 0;
    if (user.hasOwnProperty('projects')) {
        num_projects = user.projects.length
    }

    let fullname = [ user.first_name, user.last_name ].join(' ');
    if (!fullname) {
        fullname = user.shortname;
    }

    let status;
    if (user.available == 'true') {
        status = 'enabled';
    } else {
        status = 'disabled';
    }

    return (
        <Element type="user"
                 element={user}
                 isSelected={isSelected}
                 handleSelect={handleSelect}
                 status={status}
                 options={options}
        >
            {/*<Avatar className="elementIcon" email={this.props.user.email} name={fullname} round={true} size={40} color="#CFE2F3" />*/}
            <ElementTitle label={fullname} detail={user.email} />
            <ElementId id={user.id} />
            <div className="elementDetail">
                 <span className="elementLabel">Projects</span> {num_projects}
                 &nbsp;&nbsp;&nbsp;&nbsp;
                 <span className="elementLabel">Slices</span> {num_slices}
                 <br />
                 <span className="elementLabel">Organization</span> {authority}
            </div>
         </Element>
     );

 };

UserElement.propTypes = {
    user: React.PropTypes.object.isRequired
};

UserElement.defaultProps = {
};

const UserList = ({users, selected, handleSelect, options}) =>
    <List>
    {
        users.map(function(user) {

            let isSelected = false;
            if (selected) {
                 isSelected = selected.some(function (el) {
                    return el.id === user.id;
                });
            }

            return <UserElement key={user.id}
                                user={user}
                                isSelected={isSelected}
                                handleSelect={handleSelect}
                                options={options}
                    />;
        }.bind(this))
    }
    </List>;

UserList.propTypes = {
    users: React.PropTypes.array.isRequired,
};

UserList.defaultProps = {
};





const UserElementSimple = ({user}) => {

    var fullname = [ user.first_name, user.last_name ].join(' ');
    if ((!fullname) && (user.shortname)) {
        fullname = user.shortname;
    } else {
        fullname = user.email;
    }

    return <Element element={user} type="user">
                {/*<Avatar className="elementIcon" email={user.email} name={fullname} round={true} size={35} color="#CFE2F3" />*/}
                <ElementTitle label={fullname} detail={user.email} />
            </Element>;
};

UserElementSimple.propTypes = {
    user: React.PropTypes.object.isRequired
};

UserElementSimple.defaultProps = {
};

const UserListSimple = ({users}) =>
    <ListSimple>
    {
        users.map(function(user) {
            return <UserElementSimple key={user.id}
                                      user={user}
                                      status={user.status}
                    />;
        })
    }
    </ListSimple>;

UserList.propTypes = {
    users: React.PropTypes.array.isRequired
};

UserList.defaultProps = {
};


export { UserElement, UserElementSimple, UserList, UserListSimple };
