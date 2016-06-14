import React from 'react';
import store from '../stores/base/ViewStore';
import actions from '../actions/base/ViewActions';

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

    addProject(event) {
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
                        <Title title={selected.hrn} subtitle={selected.id} />
                    </PanelHeader>
                    <PanelBody>
                        <ProjectsInfo selected={selected}></ProjectsInfo>
                    </PanelBody>
                </Panel>

            ;
        }

        return (
            <View>
                <Panel>
                    <PanelHeader>
                        <Title title="Projects" />
                        <Button label="Request Project" icon="plus" active={buttonActive} handleClick={this.addProject} />
                    </PanelHeader>
                    <PanelBody>
                        <ProjectsList />
                    </PanelBody>
                </Panel>
                {panelRight}
            </View>
        );
    }
}

export default ProjectsView;