import React from 'react';

import store from '../stores/ProjectsStore';
import actions from '../actions/ProjectsActions';

import View from './base/View';
import { DialogPanel, Dialog, DialogBody, DialogHeader, DialogFooter } from './base/Dialog';
import { Panel, PanelHeader, PanelBody } from './base/Panel';
import Title from './base/Title';
import Button from './base/Button';

import ProjectsForm from './ProjectsForm';
import { ProjectList } from './objects/Project';

import { UsersSection } from './sections/User';
import { SlicesSection } from './sections/Slice';
import DateTime from './base/DateTime';

import SlicesForm from './SlicesForm';

import UsersDialog from './dialogs/SelectUser';

class ProjectsView extends React.Component {

    constructor(props) {
        super(props);
        this.state = store.getState();

        this.onChange = this.onChange.bind(this);
        this.showForm = this.showForm.bind(this);
        this.setCurrentProject = this.setCurrentProject.bind(this);
        this.closeDialog = this.closeDialog.bind(this);

        this.addUsers = this.addUsers.bind(this);
    }

    componentDidMount() {
        store.listen(this.onChange);
        this.fetchProjects();
    }

    componentWillUnmount() {
        store.unlisten(this.onChange);
    }

    onChange(state) {
        this.setState(state);
    }

    /* fetch the project list */
    fetchProjects() {
        actions.fetchProjects();
    }

    /* set the current project */
    setCurrentProject(project) {
        actions.setCurrentProject(project);
    }

    showForm() {
        actions.showDialog('project');
    }

    selectUser() {
        actions.showDialog('users');
    }

    createSlice() {
        actions.showDialog('slice');
    }

    closeDialog() {
        actions.showDialog(null);
    }

    addUsers(users) {

        this.state.saving = this.state.current.project;
        for(let i = 0; i < users.length; i++) {
            if (this.state.saving.pi_users.indexOf(users[i].id) == -1) {
               this.state.saving.pi_users.push(users[i].id);
            }
        }

        actions.saveProject();
    }

    /*
        Remove User from the current project
     */
    removeUser(user) {
        // todo
    }

    /*
        Remove Slice from the current project
     */
    removeSlice(slice) {
        // todo
        //actions.deleteSlice(slice);
    }

    render() {
        var panelRight = null;
        var dialog = null;

        if (this.state.errorMessage) {
            return (
                <div>Something is wrong</div>
            );
        }



        switch(this.state.dialog) {
            case 'users':
                dialog = <UsersDialog cancel={this.closeDialog} apply={this.addUsers} />;
                break;
            case 'slice':
                dialog = <Dialog close={this.closeDialog}>
                            <DialogPanel>
                                <DialogHeader>
                                    <Title title="New Slice" />
                                </DialogHeader>
                                <DialogBody>
                                    <SlicesForm project={this.state.current.project} close={this.closeDialog} />
                                </DialogBody>
                            </DialogPanel>
                        </Dialog>;
                break;
            case 'project':
                dialog = <Dialog close={this.closeDialog}>
                            <DialogPanel>
                                <DialogHeader>
                                    <Title title="New Project" />
                                </DialogHeader>
                                <DialogBody>
                                    <ProjectsForm close={this.closeDialog} />
                                </DialogBody>
                            </DialogPanel>
                        </Dialog>;
                break;
        }

        if (this.state.current.project) {
            let project = this.state.current.project;
            let users = this.state.current.users;
            let slices = this.state.current.slices;
            let title = project.name || project.shortname;

            /*
             *  Define options for sections USER
             * */
            let userSectionOptions = [
                {
                    'label' : 'Add User',
                    'icon' : 'plus-circle',
                    'callback' : this.selectUser
                }
            ];

            /*
             *  Define options for list element USER
             * */
            let userListOptions = [
                {
                    'label' : 'remove',
                    'callback' : this.removeUser
                }
            ];

            /*
             *  Define options for sections SLICE
             * */
            let sliceSectionOptions = [
                {
                    'label' : 'Create Slice',
                    'icon' : 'plus-circle',
                    'callback' : this.createSlice
                }
            ];

            /*
             *  Define options for list element SLICE
             * */
            let sliceListOptions = [
                {
                    'label' : 'remove',
                    'callback' : this.removeSlice
                }
            ];

            panelRight =
                <Panel>
                    <PanelHeader>
                        <Title title={title} subtitle={project.shortname} />
                        <Button label="Create Slice" icon="plus" handleClick={this.createSlice} />
                        <Button label="Add Users" icon="plus" handleClick={this.selectUser} />
                    </PanelHeader>
                    <PanelBody>
                        <div>
                            {project.id}
                            <p>
                                <a href={project.url} target="_blank">{project.url}</a>
                            </p>
                            <p>
                                {project.description}
                            </p>
                            <DateTime label="Start" timestamp={project.start_date} />
                            <DateTime label="End" timestamp={project.end_date} />
                            <SlicesSection slices={slices}
                                           sectionOptions={sliceSectionOptions}
                                           listOptions={sliceListOptions}
                            />
                            <UsersSection users={users}
                                          sectionOptions={userSectionOptions}
                                          listOptions={userListOptions}
                            />
                        </div>
                    </PanelBody>
                </Panel>;
        }

        return (
            <View>
                <Panel>
                    <PanelHeader>
                        <Title title="Projects " />
                        <Button label="Request Project" icon="plus" handleClick={this.showForm} />
                    </PanelHeader>
                    <PanelBody>
                        <ProjectList detailed={true} projects={this.state.projects} handleSelect={this.setCurrentProject} />
                    </PanelBody>
                    {dialog}
                </Panel>
                {panelRight}
            </View>
        );
    }
}

export default ProjectsView;
