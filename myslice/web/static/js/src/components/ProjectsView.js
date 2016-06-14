import React from 'react';
import store from '../stores/ProjectsStore';

import View from './base/View';
import Panel from './base/Panel';
import PanelHeader from './base/PanelHeader';
import PanelBody from './base/PanelBody';
import Title from './base/Title';

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

    render() {
        var selected = this.state.selected;

        if (this.state.errorMessage) {
            var panelRight =
                <div>Something is wrong</div>
            ;
        }

        if (selected == null) {
            var panelRight =
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
            var panelRight =
                <Panel>
                    <PanelHeader>
                        <Title title="{selected.shortname}" />
                    </PanelHeader>
                    <PanelBody>
                        <ProjectInfo key={selected} selected={selected}></ProjectInfo>
                    </PanelBody>
                </Panel>

            ;
        }

        return (
            <View>
                <Panel>
                    <PanelHeader>
                        <Title title="Projects" />
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