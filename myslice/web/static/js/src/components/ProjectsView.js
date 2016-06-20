import React from 'react';

import store from '../stores/ProjectsStore';
import actions from '../actions/ProjectsActions';

import View from './base/View';
import Panel from './base/Panel';
import PanelHeader from './base/PanelHeader';
import PanelBody from './base/PanelBody';
import Title from './base/Title';
import Button from './base/Button';

import ProjectsInfo from './ProjectsInfo';
import ProjectsForm from './ProjectsForm';
import ProjectsList from './ProjectsList';

class ProjectsView extends React.Component {

    constructor(props) {
        super(props);
        this.state = store.getState();
        this.onChange = this.onChange.bind(this);
        this.showForm = this.showForm.bind(this);
        this.selectProject = this.selectProject.bind(this);
    }

    componentDidMount() {
        store.listen(this.onChange);
        actions.fetchProjects();
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

    selectProject(project) {
        actions.selectProject(project);
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
                <Panel>
                    <PanelHeader>
                        <Title title="New Project" />
                    </PanelHeader>
                    <PanelBody>
                        <ProjectsForm />
                    </PanelBody>
                </Panel>
            ;
        } else {
            buttonActive = false;
            panelRight =
                <Panel>
                    <PanelHeader>
                        <Title title={this.state.selected.shortname} subtitle={this.state.selected.hrn} />
                    </PanelHeader>
                    <PanelBody>
                        <ProjectsInfo selected={this.state.selected} />
                    </PanelBody>
                </Panel>

            ;
        }

        return (
            <View>
                <Panel>
                    <PanelHeader>
                        <Title title="Projects" />
                        <Button label="Request Project" icon="plus" active={buttonActive} handleClick={this.showForm} />
                    </PanelHeader>
                    <PanelBody>
                        <ProjectsList projects={this.state.projects} selected={this.state.selected} selectProject={this.selectProject} />
                    </PanelBody>
                </Panel>
                {panelRight}
            </View>
        );
    }
}

export default ProjectsView;