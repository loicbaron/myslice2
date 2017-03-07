import React from 'react';
import moment from 'moment';

import { List } from '../base/List';
import { Element, ElementDetails, ElementSummary } from '../base/Element';

const ProjectElement = ({project, isSelected, handleSelect, options, userOptions, sliceOptions}) => {

        let detailsText = project.pi_users.length + ' user'+ (project.pi_users.length > 1 ? "s" : "") + ', '
                        + project.slices.length + ' slice' + (project.slices.length > 1 ? "s" : "")
                        + ', last updated ' + moment(project.updated).fromNow();


        return (
            <Element type="project"
                     element={project}
                     isSelected={isSelected}
                     handleSelect={handleSelect}
                     status={project.status}
                     options={options}>

                <ElementDetails text={detailsText}>
                    <div className="row">
                        <div className="col-sm-12">
                            <h3 className="elementLabel">
                                Managed by {project.authority.name || project.authority.shortname}
                            </h3>
                            <h4 className="elementId">
                                id: {project.id}
                            </h4>
                            <div className="row elementDate">
                                <div className="col-sm-3">
                                    <span className="elementLabel">created</span><br />
                                    {moment(project.created).calendar()}
                                </div>
                                <div className="col-sm-3">
                                    <span className="elementLabel">enabled</span><br />
                                    {moment(project.enabled).calendar()}
                                </div>
                                <div className="col-sm-3">
                                    <span className="elementLabel">updated</span><br />
                                    {moment(project.updated).calendar()}
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="row">
                        <div className="col-sm-6">
                            <ElementSummary elements={project.slices} type="slice" options={sliceOptions} />
                        </div>
                        <div className="col-sm-6">
                            <ElementSummary elements={project.pi_users} type="user" options={userOptions} />
                        </div>
                    </div>
                </ElementDetails>
            </Element>
        );

};

ProjectElement.propTypes = {
    project: React.PropTypes.object.isRequired,
    isSelected: React.PropTypes.bool,
    handleSelect: React.PropTypes.func,
    options: React.PropTypes.array,
    userOptions: React.PropTypes.array,
    sliceOptions: React.PropTypes.array,
};

ProjectElement.defaultProps = {
    options: [],
    userOptions: [],
    sliceOptions: []
};

const ProjectList = ({projects, selected, handleSelect, options, userOptions, sliceOptions}) => {

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
                                   userOptions={userOptions}
                                   sliceOptions={sliceOptions}
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
