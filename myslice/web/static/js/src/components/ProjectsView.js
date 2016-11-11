import React from 'react';

import store from '../stores/ProjectsStore';
import actions from '../actions/ProjectsActions';

import View from './base/View';
import { DialogPanel, Dialog, DialogBody, DialogHeader, DialogFooter } from './base/Dialog';
import { Panel, PanelHeader, PanelBody } from './base/Panel';
import Title from './base/Title';
import Button from './base/Button';

import ProjectsInfo from './ProjectsInfo';
import ProjectsForm from './ProjectsForm';
import { ProjectList } from './objects/Project';

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

    addUsers() {
        actions.showDialog('users');
    }
    createSlice() {
        actions.showDialog('slice');
    }
    closeDialog() {
        actions.showDialog(null);
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
                dialog = <UsersDialog close={this.closeDialog} from='authority' exclude={this.state.current.project.pi_users} addUser={true} />;
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
            let project_title = this.state.current.project.name || this.state.current.project.shortname;
            panelRight =
                <Panel>
                    <PanelHeader>
                        <Title title={project_title} subtitle={this.state.current.project.shortname} />
                        <Button label="Create Slice" icon="plus" handleClick={this.createSlice} />
                        <Button label="Add Users" icon="plus" handleClick={this.addUsers} />
                    </PanelHeader>
                    <PanelBody>
                        <ProjectsInfo element={this.state.current} />
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
