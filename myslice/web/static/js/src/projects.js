import React from 'react';
import ReactDOM from 'react-dom';
import ProjectsList from './components/ProjectsList';
import ProjectsView from './components/ProjectsView';

ReactDOM.render(
        <ProjectsList />,
        document.getElementById('projectsList')
);

ReactDOM.render(
        <ProjectsView />,
        document.getElementById('projectsView')
);