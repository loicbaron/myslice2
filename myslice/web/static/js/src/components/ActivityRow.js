import React from 'react';

import Element from './base/Element';
import ElementTitle from './base/ElementTitle';
import ElementDetails from './base/ElementDetails';
import LogList from './base/LogList';
import DateTime from './base/DateTime';

class ActivityRow extends React.Component {

    constructor(props) {
        super(props);
    }

    label() {
        var object = this.props.activity.object.type.charAt(0) + this.props.activity.object.type.slice(1).toLowerCase();
        var dataType = '';
        if (this.props.activity.data.hasOwnProperty('type')) {
            dataType = this.props.activity.data.type.charAt(0) + this.props.activity.data.type.slice(1).toLowerCase();
        }

        switch(this.props.activity.action) {
            case 'CREATE':
                return 'New ' + object;
                break;
            case 'UPDATE':
                return 'Update ' + object;
                break;
            case 'DELETE':
                return 'Delete ' + object;
                break;
            case 'ADD':
                return 'Add ' + dataType + ' to ' + object;
                break;
            case 'REMOVE':
                return 'Remove ' + dataType + ' from ' + object;
                break;
        }
    }
    render() {
        var object = this.props.activity.object.type.toLowerCase();
        var status = this.props.activity.status.toLowerCase();

        if(Object.keys(this.props.activity.data).length === 0){
            var data = this.props.activity.object;
        }else{
            var data = this.props.activity.data;
        }
        return (
            <Element element={this.props.activity}
                     type={object}
                     status={status}
                     icon={object}
            >
                <ElementTitle label={this.label()} />
                <div className="row elementDate">
                    <div className="col-sm-3">
                        <span className="elementLabel">Created</span>
                        <br />
                        <DateTime timestamp={this.props.activity.created} />
                    </div>
                    <div className="col-sm-3">
                        <span className="elementLabel">Updated</span>
                        <br />
                        <DateTime timestamp={this.props.activity.updated} />
                    </div>
                </div>
                <ElementDetails data={data} key={this.props.activity.id} />
                <LogList log={this.props.activity.log} />
            </Element>
        );
    }
 }

export default ActivityRow;
