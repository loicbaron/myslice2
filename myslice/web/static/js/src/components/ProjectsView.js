import React from 'react';
import store from '../stores/ProjectsStore';
import ProjectsForm from './ProjectsForm';
import TitlePanel from './TitlePanel';

export default class ProjectsInfo extends React.Component {

    render() {
        var p = this.props.selected;

        return (
        <div>
            <h1>{p.hrn}</h1>
            <h4>{p.id}</h4>
            <dl>
                <dt>visibility:</dt>
                <dd>{p.visibility}&nbsp;</dd>
                <dt>url:</dt>
                <dd><a href="{p.url}" target="_blank">{p.url}</a>&nbsp;</dd>
                <dt>description:</dt>
                <dd>{p.description}&nbsp;</dd>
                <dt>start:</dt>
                <dd>{p.start_date}&nbsp;</dd>
                <dt>end:</dt>
                <dd>{p.end_date}&nbsp;</dd>
            </dl>
            <div className="panel panel-default">
              <div className="panel-heading">
                <h3 className="panel-title">Users</h3>
              </div>
              <div className="panel-body">
                <ul>
                {p.pi_users.map(function(listValue, i){
                  return <li key={i}>{listValue}</li>;
                })}
                </ul>
              </div>
            </div>
            <div className="panel panel-default">
              <div className="panel-heading">
                <h3 className="panel-title">Experiments</h3>
              </div>
              <div className="panel-body">
                <ul>
                {p.slices.map(function(listValue, i){
                  return <li key={i}>{listValue}</li>;
                })}
                </ul>
              </div>
            </div>
        </div>
        );
    }
}

module.exports = React.createClass({
    getInitialState: function() {
        return store.getState();
    },

    componentDidMount: function() {
        // listen on state changes
        store.listen(this.onChange);
    },

    componentWillUnmount() {
        store.unlisten(this.onChange);
    },

    onChange(state) {
        this.setState(state);
    },

    render: function() {
        var selected = this.state.selected;

        if (this.state.errorMessage) {
            return (
                <div>Something is wrong</div>
            );
        }

        if (selected == null) {
            return(
                <div>
                    <TitlePanel title="New Project" />
                    <ProjectsForm />
                </div>
            )
        } else {
            return (
                <ProjectInfo key={selected} selected={selected}></ProjectInfo>
            );
        }
    }
});