var ReactDOM = require('react-dom');
var React = require('react');
var ProjectsList = require('./components/ProjectsList');
var ProjectsView = require('./components/ProjectsView');

ReactDOM.render(
        <ProjectsList />,
        document.getElementById('projectsList')
);

ReactDOM.render(
        <ProjectsView />,
        document.getElementById('projectsView')
);