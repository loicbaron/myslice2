import React from 'react';

import store from '../stores/base/ElementStore';
import actions from '../actions/base/ElementActions';

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

    showForm() {
        actions.selectElement(null);
    }

    // selectUser(user) {
    //     actions.selectElement(user);
    // }

    getSelectedId() {
        if (this.state.selected) {
            return this.state.selected.id;
        } else {
            return null;
        }
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

        var selectedId = null;
        if (this.state.selected) {
            selectedId = this.state.selected.id;
        }

        return (
            <View>
                <Panel>
                    <PanelHeader>
                        <Title title="Users" />
                    </PanelHeader>
                    <PanelBody>
                        <UsersList select={true} />
                    </PanelBody>
                </Panel>
                {panelRight}
            </View>
        );
    }
}

export default UsersView;
