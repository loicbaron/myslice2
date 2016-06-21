import React from 'react';

class UsersInfo extends React.Component {

    render() {
        var p = this.props.selected;

        return (
        <div>
            <dl>
                <dt>Name:</dt>
                <dd>{p.first_name}&nbsp;{p.last_name}</dd>
                <dt>Email:</dt>
                <dd>{p.email}&nbsp;</dd>
            </dl>
            <div className="panel panel-default">
              <div className="panel-heading">
                <h3 className="panel-title">Projects</h3>
              </div>
              <div className="panel-body">
                <ul>
                {p.projects.map(function(listValue, i){
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

export default UsersInfo;
