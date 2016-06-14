import React from 'react';
import moment from 'moment';

class ProjectLabel extends React.Component {

    label() {
        let label = '';
        switch(this.props.project.action) {
            case 'REQ':
                label = 'requested ' + this.props.project.object.type;
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

class ProjectStatus extends React.Component {

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


class ProjectsRow extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            'selected': false
        };
        this.handleClick = this.handleClick.bind(this);
    }

    handleClick(){

        if (this.state.selected == this.props.project) {
            this.setState({
                'selected': false
            });
        } else {
            this.setState({
                'selected': this.props.project
            });
        }
        /*
        if(this.state.selected){
            this.setState({'selected':false});
        }else{
            this.setState({'selected':true});
        }
        */
    }

    render() {
         if(this.props.selected == this.props.project){
            var liClass = 'elementBox selected';
         }else{
            var liClass = 'elementBox';
         }
         return (
             <li className={liClass} onClick={this.handleClick}>
                 <ProjectLabel project={this.props.project} />
                 <div className="row">
                     <div className="col-md-6">
                         <div className="elementId">
                             {this.props.project.id}
                         </div>
                         <div className="elementDate">
                            Created: { moment(this.props.project.created).format("DD/MM/YYYY H:mm") }
                            <br />
                            Updated: { moment(this.props.project.updated).format("DD/MM/YYYY H:mm") }
                         </div>
                     </div>
                     <div className="col-md-6">

                     </div>
                 </div>
                 <ProjectStatus status={this.props.project.status} />
             </li>
         );
    }
 }

export default ProjectsRow;