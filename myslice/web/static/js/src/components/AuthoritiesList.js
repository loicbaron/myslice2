import React from 'react';

import List from './base/List';
import AuthoritiesRow from'./AuthoritiesRow';

class AuthoritiesList extends React.Component {

    render() {

        if (!this.props.authorities || this.props.authorities.length==0) {
            return <List>No authority</List>
        } else {
            return (
                <List>
                {
                    this.props.authorities.map(function(authority) {
                        return <AuthoritiesRow key={authority.id} authority={authority} setCurrent={this.props.setCurrent} current={this.props.current} />;
                    }.bind(this))
                }
                </List>
            );
        }

    }
}

AuthoritiesList.propTypes = {
    authorities: React.PropTypes.array.isRequired,
    current: React.PropTypes.object,
    setCurrent: React.PropTypes.func
};

AuthoritiesList.defaultProps = {
    current: null,
    setCurrent: null
};

export default AuthoritiesList;
