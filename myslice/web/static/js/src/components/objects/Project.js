import React from 'react';

import { List, ListSimple } from '../base/List';
import { Element } from '../base/Element';
import ElementTitle from '../base/ElementTitle';
import ElementId from '../base/ElementId';
import DateTime from '../base/DateTime';

const ProjectElement = ({project, isSelected, handleSelect, options}) => {

        let label = project.name || project.shortname;
        let authority = project.authority.name || project.authority.shortname;


        let users;
        if(project.pi_users){
            users = <span className="elementLabel">Users {project.pi_users.length} </span>
        }
        let slices;
        if(project.slices){
            slices = <span className="elementLabel">Slices: {project.slices.length}</span>
        }
        let slicesInDashboard;
        console.log(project);
        if(project.slices){
            slicesInDashboard = <div>
            {
                project.slices.map(function (slice) {
                    var slice_link="/slices/"+slice.hrn;
                    return <span key={slice.id } className="elementLabel"><a href={slice_link}><i className="fa fa-tasks fa-lg"></i>&nbsp;{slice.shortname}</a>&nbsp;</span>;
                }.bind(this))
            }
            </div>;
            //slicesInDashboard = <span className="elementLabel">Slices: {SliceLabel}</span>
        }
        var created;
        if(project.created){
            created = <div className="col-sm-3"><DateTime label="Created" timestamp={project.created}/></div>
        }
        var enabled;
        if(project.enabled){
            created = <div className="col-sm-3"><DateTime label="Enabled" timestamp={project.enabled}/></div>
        }
        var updated;
        if(project.updated){
            created = <div className="col-sm-3"><DateTime label="Updated" timestamp={project.updated}/></div>
        }
        var authorityElement;
        if(authority){
            authorityElement = <span className="elementLabel">Managed by {authority}</span>
        }
        var projectElements;
        if(users || slices || authorityElement){
            projectElements = <div className="elementDetail">{users}&nbsp;&nbsp;{slices}<br/>{authorityElement}</div>
        }
        var detailed = true;
        for(var i in options){
            if (options[i].hasOwnProperty('detailed') && options[i]['detailed']==false){
                detailed = false;
            }
        }
        if (detailed){
            return (
                <Element type="project"
                         element={project}
                         isSelected={isSelected}
                         handleSelect={handleSelect}
                         status={project.status}
                         options={options}
                         icon="project"
                >
                    <ElementTitle label={label} detail={project.shortname}/>
                    <ElementId id={project.id}/>
                    {projectElements}
                    <div className="row elementDate">
                        {created}
                        {enabled}
                        {updated}
                    </div>
                </Element>
            );
        }else{
            return (
                <Element type="project"
                         element={project}
                         isSelected={isSelected}
                         handleSelect={handleSelect}
                         options={options}
                         icon="project">

                    <a href="/projects"><ElementTitle label={label} detail={project.shortname} /></a>

                    <ElementId id={project.id} />

                    <div> {slicesInDashboard}</div>

                </Element>
            );
        }
};

ProjectElement.propTypes = {
    project: React.PropTypes.object.isRequired,
    handleClick: React.PropTypes.func,
    removeProject: React.PropTypes.bool
};

ProjectElement.defaultProps = {
    removeProject: true
};

const ProjectList = ({projects, selected, handleSelect, options}) => {

    let iconSelected = "arrow";

    if (selected) {
        if (selected instanceof Array) {
            iconSelected = "check";
        } else {
            selected = [selected];
        }
    }

    return (<List>
    {
        projects.map(function(project) {

            let isSelected = false;
            if (selected) {
                isSelected = selected.some(function (el) {
                    return el.id === project.id;
                });
            }

            return <ProjectElement key={project.id}
                                   project={project}
                                   isSelected={isSelected ? iconSelected : null}
                                   iconSelected={iconSelected}
                                   handleSelect={handleSelect}
                                   options={options}
                    />;

        })
    }
    </List>);
};

ProjectList.propTypes = {
    projects: React.PropTypes.array.isRequired,
};

ProjectList.defaultProps = {
};

export { ProjectElement, ProjectList };
