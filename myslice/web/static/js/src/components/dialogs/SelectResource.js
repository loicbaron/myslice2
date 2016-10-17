import React from 'react';

import actions from '../../actions/dialogs/SelectResource';
import store from '../../stores/dialogs/SelectResource';

import Dialog from '../base/Dialog';
import DialogPanel from '../base/DialogPanel';
import DialogHeader from '../base/DialogHeader';
import DialogBody from '../base/DialogBody';
import Title from '../base/Title';
import List from '../base/List';

import ResourceElement from '../objects/ResourceElement';

class SelectResourceDialog extends React.Component {

    constructor(props) {
        super(props);
        this.state = store.getState();
        this.onChange = this.onChange.bind(this);
        //this.handleFilter = this.handleFilter.bind(this);
    }

    componentDidMount() {
        store.listen(this.onChange);
        actions.fetchResources(this.props.testbed);
    }

    componentWillUnmount() {
        store.unlisten(this.onChange);
    }

    onChange(state) {
        this.setState(state);
    }

    handleFilter(value) {
        var f = {'email':value,'shortname':value}
        actions.updateFilter(f);
        actions.updateFilteredUsers();
    }
    /* fetch the users list */
    fetchUsers(filter={}) {
        switch (this.props.from){
            case 'authority':
                actions.fetchFromAuthority(filter);
                break;
            default:
                actions.fetchUsers(filter);
        }
    }

    selectResource(resource) {
        actions.selectResource(resource);
    }

    isSelected(resource) {
        //console.log(this.state.selected);
        /* TOFIX
        this.state.selected.find((el) => {
            return el.id === resource.id;
        })
        */
    }

    render() {
        // if(Object.keys(this.state.filter).length>0){
        //     var usersList = <UsersList users={this.state.filteredUsers} addUser={this.props.addUser} />
        // }else{
        //     var usersList = <UsersList users={this.state.users} addUser={this.props.addUser} />
        // }

        return (
            <Dialog close={this.props.close}>
                <DialogPanel>
                    <DialogHeader>
                        <Title title={this.props.testbed.name} />
                    </DialogHeader>
                    <DialogBody>
                        <List>
                        {
                            this.state.resources.map(function(resource) {

                                return <ResourceElement key={resource.id}
                                                        resource={resource}
                                                        handleClick={() => this.selectResource(resource)} />;
                            }.bind(this))
                        }
                        </List>
                    </DialogBody>
                </DialogPanel>
            </Dialog>
        );
    }
}

SelectResourceDialog.propTypes = {
    testbed: React.PropTypes.object.isRequired,
    close: React.PropTypes.func.isRequired,
};

SelectResourceDialog.defaultProps = {

};

export default SelectResourceDialog;
