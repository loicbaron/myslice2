import React from 'react';

import Element from './base/Element';
import ElementTitle from './base/ElementTitle';
import ElementStatus from './base/ElementStatus';
import ElementIcon from './base/ElementIcon';
import LogList from './base/LogList';
import DateTime from './base/DateTime';

class RequestsRow extends React.Component {

    constructor(props) {
        super(props);
    }

    label() {
        var object = this.props.request.object.type.charAt(0) + this.props.request.object.type.slice(1).toLowerCase();
        var data = '';
        if (this.props.request.data.hasOwnProperty('type')) {
            data = this.props.request.data.type.charAt(0) + this.props.request.data.type.slice(1).toLowerCase();
        }

        switch(this.props.request.action) {
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
                return 'Add ' + data + ' to ' + object;
                break;
            case 'REMOVE':
                return 'Remove ' + data + ' from ' + object;
                break;
        }
    }


    approve(e){
        e.preventDefault();
        this.props.executeAction({   
                id : this.props.request.id,
                action: 'approve',
                message: this.refs.message.value
            })
    }


    deny(e){
        e.preventDefault();
        this.props.executeAction(
            {   
                id : this.props.request.id,
                action: 'deny',
                message: this.refs.message.value
            })
    }

    render() {
        var object = this.props.request.object.type.toLowerCase();
        var status = this.props.request.status.toLowerCase();

        var executePanel = <div></div>; 

        if (this.props.request.executable) {
            var executePanel = (
                        <div>
                            <div className="row">
                                <div className="col-sm-6 col-sm-offset-6">
                                    <input  type="text"
                                            name="message"
                                            ref="message"
                                                />
                                    </div>
                            </div>

                            <div className="row">
                                <div className="col-sm-3 col-sm-offset-6">
                                    <button type="button" 
                                            className="btn btn-default"
                                            name="approve"
                                            value="approve"
                                            onClick={this.approve.bind(this)}>Approve</button>
                                </div>
                                <div className="col-sm-3">
                                    <button type="button"
                                            className="btn btn-default"
                                            name="deny"
                                            value="deny"
                                            onClick={this.deny.bind(this)}>Deny</button>
                                </div>
                            </div>
                            
                        </div>); 
        }

        return (
            <Element element={this.props.request} type={object}>
                <ElementStatus status={status} />
                <ElementIcon icon={object} />
                <ElementTitle label={this.label()} />
                <div className="row elementDate">
                    <div className="col-sm-3">
                        <DateTime label="Created" timestamp={this.props.request.created}/>
                    </div>
                    <div className="col-sm-3">
                        <DateTime label="Updated" timestamp={this.props.request.updated}/>
                    </div>
                </div>
                {executePanel}
                <LogList log={this.props.request.log} />
            </Element>
        );
    }
 }

RequestsRow.propTypes = {
    executeAction: React.PropTypes.func
}

export default RequestsRow;