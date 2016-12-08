import React from 'react';

import actions from '../../actions/dialogs/SelectUser';
import store from '../../stores/dialogs/SelectUser';

import { DialogPanel, Dialog, DialogBody, DialogHeader, DialogBar, DialogFooter } from '../base/Dialog';
import Title from '../base/Title';
import { UserList } from '../objects/User';

import SelectAuthority from '../forms/SelectAuthority';

class SelectUserDialog extends React.Component {

    constructor(props) {
        super(props);
        this.state = store.getState();
        this.onChange = this.onChange.bind(this);
        this.showSelected = this.showSelected.bind(this);
        this.cancel = this.cancel.bind(this);
        this.apply = this.apply.bind(this);
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

    filterAuthority(authority) {
        actions.filterAuthority(authority);
    }

    filterUser(event) {
        actions.filterUser(event.target.value);
    }

    selectUser(user) {
        actions.selectUser(user);
    }

    clearSelection() {
        actions.clearSelection();
    }

    showSelected() {
        actions.showSelected();
    }

    showAll() {
        actions.showAll();
    }

    renderSelectedStatus() {
        if (this.state.selected.length > 0) {
            if (this.state.show_selected) {
                return <div className="d-selected">
                    You have selected <span>{this.state.selected.length + " user" + (this.state.selected.length > 1 ? "s" : "")}</span>
                    &nbsp;(<a onClick={this.showAll}>Show all users</a> | <a onClick={this.clearSelection}>Clear</a>)
                </div>;
            } else {
                return <div className="d-selected">
                    You have selected <a onClick={this.showSelected}>{this.state.selected.length + " user" + (this.state.selected.length > 1 ? "s" : "")}</a>
                </div>;
            }
        } else {
            return <div className="d-selected">Select users</div>;
        }
    }

    cancel() {
        this.clearSelection();
        this.props.cancel();
    }

    apply() {
        this.props.apply(this.state.selected);
        this.clearSelection();
        this.props.cancel();
    }

    render() {
        let users = [];
        if (this.state.show_selected) {
            users = this.state.selected;
        } else if (this.state.filtered.length > 0) {
            users = this.state.filtered;
        } else {
            users = this.state.users;
        }

        return (
            <Dialog cancel={this.cancel}>
                <DialogHeader>
                    <Title title="Add Users" />
                </DialogHeader>
                <DialogBar>
                    <SelectAuthority placeholder="Filter by Organization"
                                     value={this.state.authority}
                                     handleChange={this.filterAuthority} />
                    <input
                        type="text"
                        onChange={this.filterUser}
                        placeholder="Filter by name or email"
                    />
                </DialogBar>
                <DialogBody>
                    <UserList users={users}
                              selected={this.state.selected}
                              handleSelect={this.selectUser}
                    />
                </DialogBody>
                <DialogFooter>
                    {this.renderSelectedStatus()}
                    <div>
                        <button className="cancel" onClick={this.cancel} >
                            Cancel
                        </button>
                        <button className="apply" onClick={this.apply} >
                            Apply
                        </button>
                    </div>
                </DialogFooter>
            </Dialog>
        );
    }
}

SelectUserDialog.propTypes = {
    apply: React.PropTypes.func.isRequired,
    cancel: React.PropTypes.func.isRequired
};

SelectUserDialog.defaultProps = {

};

export default SelectUserDialog;
