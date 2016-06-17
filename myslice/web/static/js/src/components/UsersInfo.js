import React from 'react';

class UsersInfo extends React.Component {

    render() {
        var p = this.props.selected;

        return (
        <div>
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

export default UsersInfo;
