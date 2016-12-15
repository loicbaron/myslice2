import React from 'react';

import store from '../stores/UsersStore';
import actions from '../actions/UsersActions';

import View from './base/View';
import { Panel, PanelHeader, PanelBody } from './base/Panel';
import Title from './base/Title';
import Button from './base/Button';

import UsersInfo from './UsersInfo';
import { UserList } from './objects/User';

import SelectAuthority from './forms/SelectAuthority';

class UsersView extends React.Component {

    constructor(props) {
        super(props);
        this.state = store.getState();
        this.onChange = this.onChange.bind(this);
        this.showForm = this.showForm.bind(this);
        this.setCurrentUser = this.setCurrentUser.bind(this);
        actions.fetchProfile.defer();
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
    filterUser(event) {
        actions.filterUser(event.target.value);
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
        let users = [];
        if (this.state.filtered.length > 0) {
            users = this.state.filtered;
        } else {
            users = this.state.users;
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
                        <UsersInfo element={this.state.current.user} />
                    </PanelBody>
                </Panel>
            ;
        } else {
            buttonActive = true;
            panelRight =
                <div />
            ;
        }
        console.log("render UsersView");
        console.log(this.state.profile);
        var selectAuthority = <SelectAuthority handleChange={this.updateAuthority} selected={this.state.authority} />
        if(Object.keys(this.state.profile).length>0){
            console.log(this.state.profile.pi_authorities);
        } 
        if(Object.keys(this.state.profile).length>0 && this.state.profile.pi_authorities.length>0){
            for(var e in this.state.profile.pi_authorities){
                var p = this.state.profile.pi_authorities[e];
                console.log(typeof(p));
                if(typeof(p) === 'object'){
                    if('hrn' in p && p['hrn'].split('.').length == 1){
                        console.log('is root admin');
                        var is_root = true;
                        break;
                    }else{
                        var is_root = false;
                    }
                }else{
                    // root authority
                    // urn:publicid:IDN+onelab+authority+sa
                    if(p.split('+')[1].split(':').length == 1){
                        var is_root = true;
                        break;
                    }else{
                        // urn:publicid:IDN+onelab:upmc+authority+sa
                        var is_root = false;
                    }
                }
            }
            if(is_root){
                return (
                    <View>
                        <Panel>
                            <PanelHeader>
                                <Title title="Users" />
                            </PanelHeader>
                            <PanelBody>
                                <div className="row">
                                    <div className="col-sm-10 col-sm-offset-1 inputForm">
                                    {selectAuthority}
                                    <input
                                        type="text"
                                        onChange={this.filterUser}
                                        placeholder="Filter by name or email"
                                    />
                                    </div>
                                </div>
                                <UserList select={true} users={users} handleSelect={this.setCurrentUser} current={this.state.current.user} />
                            </PanelBody>
                        </Panel>
                        {panelRight}
                    </View>
                );
            }else{
                return (
                    <View>
                        <Panel>
                            <PanelHeader>
                                <Title title="Users" subtitle={this.state.profile.authority.name} />
                            </PanelHeader>
                            <PanelBody>
                                <div className="row">
                                </div>
                                <UserList select={true} users={users} handleSelect={this.setCurrentUser} current={this.state.current.user} />
                            </PanelBody>
                        </Panel>
                        {panelRight}
                    </View>
                );
            }
        }else{
            return(
                <View>
                    <Panel>
                        <PanelHeader>
                            <Title title="Users" />
                        </PanelHeader>
                        <PanelBody>
                            <div className="row">
                                <div className="col-sm-10 col-sm-offset-1 inputForm">You don't have rights to manage users
                                </div>
                            </div>
                        </PanelBody>
                    </Panel>
                    <Panel></Panel>
                </View>
            );
        }

    }
}

export default UsersView;
