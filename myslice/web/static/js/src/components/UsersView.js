import React from 'react';

import store from '../stores/UsersStore';
import actions from '../actions/UsersActions';

import View from './base/View';
import Panel from './base/Panel';
import PanelHeader from './base/PanelHeader';
import PanelBody from './base/PanelBody';
import Title from './base/Title';
import Button from './base/Button';

import UsersInfo from './UsersInfo';
import UsersList from './UsersList';

import AuthoritiesSelect from './AuthoritiesSelect';

class UsersView extends React.Component {

    constructor(props) {
        super(props);
        this.state = store.getState();
        this.onChange = this.onChange.bind(this);
        this.showForm = this.showForm.bind(this);
        this.setCurrentUser = this.setCurrentUser.bind(this);
        actions.fetchProfile();
        //actions.fetchFromUserAuthority();
        // this.selectUser = this.selectUser.bind(this);
    }

    componentDidMount() {
        store.listen(this.onChange);
    }

    componentWillUnmount() {
        store.unlisten(this.onChange);
    }

    onChange(state) {
        this.setState(state);
    }
    updateAuthority(value) {
        actions.updateAuthority(value);
        if(value){
            actions.fetchFromAuthority();
        }else{
            actions.updateUsers([]);
        }
    }

    /* set the current user */
    setCurrentUser(user) {
        actions.setCurrentUser(user);
    }

    showForm() {
        actions.selectElement(null);
    }

    // selectUser(user) {
    //     actions.selectElement(user);
    // }

    render() {
        var buttonActive = false;
        var panelRight = null;

        if (this.state.errorMessage) {
            return (
                <div>Something is wrong</div>
            );
        }

        if (this.state.current.user) {
            let user_title = this.state.current.user.first_name+" "+this.state.current.user.last_name;
            buttonActive = false;
            panelRight =
                <Panel>
                    <PanelHeader>
                        <Title title={user_title} subtitle={this.state.current.user.hrn} />
                    </PanelHeader>
                    <PanelBody>
                        <UsersInfo selected={this.state.current.user} />
                    </PanelBody>
                </Panel>
            ;
        } else {
            buttonActive = true;
            panelRight =
                <div />
            ;
        }

        return (
            <View>
                <Panel>
                    <PanelHeader>
                        <Title title="Users" />
                    </PanelHeader>
                    <PanelBody>
                        <div className="row">
                            <div className="col-sm-10 col-sm-offset-1 inputForm">
                                <AuthoritiesSelect handleChange={this.updateAuthority} selected={this.state.authority} />
                            </div>
                        </div>
                        <UsersList select={true} users={this.state.users} setCurrent={this.setCurrentUser} current={this.state.current.user} />
                    </PanelBody>
                </Panel>
                {panelRight}
            </View>
        );
    }
}

export default UsersView;
