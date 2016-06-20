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

class UsersView extends React.Component {

    constructor(props) {
        super(props);
        this.state = store.getState();
        this.onChange = this.onChange.bind(this);
        this.showForm = this.showForm.bind(this);
        this.selectUser = this.selectUser.bind(this);
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

    showForm() {
        this.state.selected = null;
    }

    selectUser(user) {
        actions.selectUser(user);
    }

    render() {
        var buttonActive = false;
        var panelRight = null;

        if (this.state.errorMessage) {
            return (
                <div>Something is wrong</div>
            );
        }

        if (this.state.selected == null) {
            buttonActive = true;
            panelRight =
                <div />
            ;
        } else {
            buttonActive = false;
            panelRight =
                <Panel>
                    <PanelHeader>
                        <Title title={this.state.selected.shortname} subtitle={this.state.selected.hrn} />
                    </PanelHeader>
                    <PanelBody>
                        <UsersInfo selected={this.state.selected} />
                    </PanelBody>
                </Panel>

            ;
        }

        return (
            <View>
                <Panel>
                    <PanelHeader>
                        <Title title="Users" />
                    </PanelHeader>
                    <PanelBody>
                        <UsersList users={this.state.users} selected={this.state.selected} selectUser={this.selectUser} />
                    </PanelBody>
                </Panel>
                {panelRight}
            </View>
        );
    }
}

export default UsersView;
