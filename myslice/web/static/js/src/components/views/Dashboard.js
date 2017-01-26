/**
 * Created by amirabradai on 14/10/2016.
 */
import React from 'react';

import store from '../../stores/views/Dashboard';
import actions from '../../actions/views/Dashboard';

import { View, ViewHeader, ViewBody, Panel } from '../base/View';
import { DialogPanel, Dialog, DialogBody, DialogHeader, DialogFooter } from '../base/Dialog';
import Title from '../base/Title';
import Button from '../base/Button';
import Text from '../base/Text';
import ProjectsForm from '../ProjectsForm';
import { ProjectList } from '../objects/Project';


class DashboardView extends React.Component {
    constructor(props) {
        super(props);
        //this.state = store.getState;
        this.state ={};
        this.onChange = this.onChange.bind(this);
        this.showForm = this.showForm.bind(this);
        //this.setCurrentProject = this.setCurrentProject.bind(this);
        //this.closeDialog = this.closeDialog.bind(this);
    }
    /* fetch the project list */
    fetchProjects() {
        actions.fetchProjects();
    }

    /*Fetch the slices of the each projects*/
    fetchSlicesByProject() {
        actions.fetchSlicesByProject();
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
    showForm() {
        actions.showDialog('project');
    }
    closeDialog() {
        actions.showDialog(null);
    }

    render()
    {   var panelRight = null;
        var dialog = null;

        if (this.state.errorMessage) {
            return (
                <div>Something is wrong</div>
            );
        }
// When we want to add a project
        if (this.state.dialog=='project'){
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
        }
        var projectsList = '';
        var options = [{'detailed':false}];
        if(this.state.projects){
            projectsList = <ProjectList options={options} projects={this.state.projects}  />
        }
// The view of the dashboard page
        return (

        <View>
            <ViewHeader>
                <Title title="Dashboard" />
            </ViewHeader>
            <ViewBody>
                <Panel>
                    <p>
                        Through OneLab, you can easily test the software system that you have designed
                        that you have designed to function in any one of the following networked
                        communication environments:
                    </p>
                    <ul>
                        <li>
                            IoT networks with mobility and sensing capabilities;
                        </li>
                        <li>
                            ad-hoc wireless and wireless broadband access networks;
                        </li>
                        <li>
                            a global, public, fixed-line Internet;
                        </li>
                        <li>
                            and Cloud and SDN networks.
                        </li>
                    </ul>
                    <p>
                        Our platforms offer both wireless and fixed-line emulated environments and
                        reproducibility of experimentation.
                    </p>
                </Panel>
                <Panel>
                    <Title title="Projects & Slices"/>
                    <Button label="Request Project" icon="plus" handleClick={this.showForm} />
                    {projectsList}
            </Panel>
            </ViewBody>
             {dialog}
        </View>
        );


    }

};
module.exports = DashboardView;
