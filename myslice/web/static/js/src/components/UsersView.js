import React from 'react';
import store from '../stores/base/ViewStore';
import actions from '../actions/base/ViewActions';

import View from './base/View';
import Panel from './base/Panel';
import PanelHeader from './base/PanelHeader';
import PanelBody from './base/PanelBody';
import Title from './base/Title';
import Button from './base/Button';

import UsersInfo from './UsersInfo';
//import UsersForm from './UsersForm';
import UsersList from './UsersList';

class UsersView extends React.Component {

    constructor(props) {
        super(props);
        this.state = store.getState();
        this.onChange = this.onChange.bind(this);
    }

    componentDidMount() {
        // listen on state changes
        store.listen(this.onChange);
    }

    componentWillUnmount() {
        store.unlisten(this.onChange);
    }

    onChange(state) {
        this.setState(state);
    }

    showForm() {
        actions.updateSelectedElement(null);
    }

    render() {
        var selected = this.state.selectedElement;
        var buttonActive = false;
        var panelRight = null;

        if (this.state.errorMessage) {
            return (
                <div>Something is wrong</div>
            );
        }

        if (selected == null) {
            buttonActive = true;
            panelRight =
                <Panel>
                </Panel>
            ;
        } else {
            buttonActive = false;
            panelRight =
                <Panel>
                    <PanelHeader>
                        <Title title={selected.hrn} subtitle={selected.id} />
                    </PanelHeader>
                    <PanelBody>
                        <UsersInfo selected={selected}></UsersInfo>
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
                        <UsersList />
                    </PanelBody>
                </Panel>
                {panelRight}
            </View>
        );
    }
}

export default UsersView;
