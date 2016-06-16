import React from 'react';
import moment from 'moment';

import Element from './base/Element';
import Log from './base/Log';

class ActivityLabel extends React.Component {

    label() {
        let label = '';
        switch(this.props.activity.action) {
            case 'REQ':
                label = 'requested ' + this.props.activity.object.type;
        }
        return label;
    }

    render() {
        return (

            <div className="row">
                <div className="col-md-12">
                    <div className="elementIcon">
                <img src="/static/icons/projects-w-24.png" alt="" />
            </div>
                    <div className="elementLabel">{ this.label() }</div>
                </div>
            </div>
        )
    }
}

class ActivityStatus extends React.Component {

    render() {
        return (
            <div className="row">
                <div className="col-md-12">
                    <div className="elementStatus">{ this.props.status }</div>
                </div>
            </div>
        )
    }
}


class ActivityRow extends React.Component {

    constructor(props) {
        super(props);
    }


    render() {

         return (
             <Element element={this.props.project}>
                 <ActivityLabel activity={this.props.activity} />
                 <div className="row">
                     <div className="col-md-6">
                         <div className="elementId">
                             {this.props.activity.id}
                         </div>
                         <div className="elementDate">
                            Created: { moment(this.props.activity.created).format("DD/MM/YYYY H:mm") }
                            <br />
                            Updated: { moment(this.props.activity.updated).format("DD/MM/YYYY H:mm") }
                         </div>
                     </div>
                     <div className="col-md-6">

                     </div>
                 </div>
                 <ActivityStatus status={this.props.activity.status} />
                 {
                     this.props.activity.log.map(function(log) {
                         return <Log key={log.timestamp} log={log} />;
                     })
                 }
             </Element>
         );
    }
 }

export default ActivityRow;