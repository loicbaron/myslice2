import React from 'react';

import store from '../stores/ProjectsStore';
import actions from '../actions/ProjectsActions';

import View from './base/View';
import { DialogConfirm, DialogPanel, Dialog, DialogBody, DialogHeader, DialogFooter } from './base/Dialog';
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
        actions.showDialog({name: 'project'});
    }

    closeDialog() {
        actions.closeDialog();
    }

    /*
     * Projects actions and dialogs
     */
    deleteProjectConfirm(project) {
        actions.showDialog({name: 'deleteProjectConfirm', project: project});
    }

    deleteProject(project) {
        actions.deleteProject(project);
        actions.closeDialog();
    }

    /**
     * User actions and dialogs
     */
    selectUserDialog() {
        actions.showDialog({name: 'users'});
    }

    addUsers(users) {
        actions.saveProject({users: users});
        actions.closeDialog();
    }

    removeUserConfirm(user) {
        actions.showDialog({name: 'removeUserConfirm', user: user});
    }

    removeUser(user) {
        actions.saveProject({remove_user: user});
        actions.closeDialog();
    }

    /**
     * Slice actions and dialogs
     */
    createSliceDialog() {
        actions.showDialog({name: 'slice'});
    }

    deleteSliceConfirm(slice) {
        actions.showDialog({name: 'deleteSliceConfirm', slice: slice});
    }

    deleteSlice(slice) {
        actions.deleteSlice(slice);
        actions.closeDialog();
    }

    render() {
        let panelRight = null;
        let dialog = null;

        if (this.state.errorMessage) {
            return (
                <div>Something is wrong</div>
            );
        }


        switch(this.state.dialog.name) {
            case 'users':
                dialog = <UsersDialog apply={this.addUsers} cancel={this.closeDialog} />;
                break;
            case 'removeUserConfirm':
                let fullname = [ this.state.dialog.user.first_name, this.state.dialog.user.last_name ].join(' ');
                if (!fullname) {
                    fullname = this.state.dialog.user.shortname;
                }
                dialog = <DialogConfirm confirm={() => this.removeUser(this.state.dialog.user)} cancel={this.closeDialog}>
                    <p>
                        The user {fullname} ({this.state.dialog.user.email})
                        will be removed from the project {this.state.current.project.label}
                        ({this.state.current.project.shortname}) and he won't be able to access it anymore.
                    </p>
                    <p>
                        Are you sure you want to continue?
                    </p>
                </DialogConfirm>;
                break;
            case 'slice':
                dialog = <Dialog cancel={this.closeDialog}>
                            <DialogHeader>
                                <Title title="New Slice" />
                            </DialogHeader>
                            <DialogBody>
                                <SlicesForm project={this.state.current.project} close={this.closeDialog} />
                            </DialogBody>
                        </Dialog>;
                break;
            case 'deleteSliceConfirm':
                dialog = <DialogConfirm confirm={() => this.deleteSlice(this.state.dialog.slice)} cancel={this.closeDialog}>
                    <p>
                        The slice ({this.state.dialog.slice.shortname}) will be deleted
                        <br />
                        All associated resources will be removed and data deployed on the resources will be lost.
                    </p>
                    <p>
                        Are you sure you want to continue?
                    </p>
                </DialogConfirm>;
                break;
            case 'deleteProjectConfirm':
                dialog = <DialogConfirm confirm={() => this.deleteProject(this.state.dialog.project)} cancel={this.closeDialog}>
                    <p>
                        The project ({this.state.dialog.project.shortname}) will be deleted
                        <br />
                        All associated slices and resources will be removed and data deployed on the resources will be lost.
                        <br />
                        The users associated with the project will not be able to access it anymore.
                    </p>
                    <p>
                        Are you sure you want to continue?
                    </p>
                </DialogConfirm>;
                break;
            case 'project':
                dialog = <Dialog cancel={this.closeDialog}>
                            <DialogHeader>
                                <Title title="New Project" />
                            </DialogHeader>
                            <DialogBody>
                                <ProjectsForm close={this.closeDialog} />
                            </DialogBody>
                        </Dialog>;
                break;
        }

        /*
         *  Define options for list element SLICE
         * */
        let projectListOptions = [
            {
                'label' : 'delete',
                'callback' : this.deleteProjectConfirm
            }
        ];

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
                    'icon' : 'add',
                    'callback' : this.selectUserDialog
                }
            ];

            /*
             *  Define options for list element USER
             * */
            let userListOptions = [
                {
                    'label' : 'remove',
                    'callback' : this.removeUserConfirm
                }
            ];

            /*
             *  Define options for sections SLICE
             * */
            let sliceSectionOptions = [
                {
                    'label' : 'Create Slice',
                    'icon' : 'create',
                    'callback' : this.createSliceDialog
                }
            ];

            /*
             *  Define options for list element SLICE
             * */
            let sliceListOptions = [
                {
                    'label' : 'delete',
                    'callback' : this.deleteSliceConfirm
                }
            ];

            panelRight =
                <Panel>
                    <PanelHeader>
                        <Title title={title} subtitle={project.shortname} />
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
            <View notification={this.state.notification}>
                <Panel>
                    <PanelHeader>
                        <Title title="Projects " />
                        <Button label="Request Project" icon="plus" handleClick={this.showForm} />
                    </PanelHeader>
                    <PanelBody>
                        <ProjectList projects={this.state.projects}
                                     selected={this.state.current.project}
                                     handleSelect={this.setCurrentProject}
                                     options={projectListOptions}
                        />
                    </PanelBody>
                    {dialog}
                </Panel>
                {panelRight}
            </View>
        );
    }
}

export default ProjectsView;
