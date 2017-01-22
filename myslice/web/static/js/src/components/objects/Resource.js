import React from 'react';

import Title from '../base/Title';
import { List, ListSimple } from '../base/List';
import { Element } from '../base/Element';
import ElementTitle from '../base/ElementTitle';
import ElementId from '../base/ElementId';
import DateTime from '../base/DateTime';
import { Icon } from '../base/Icon';

const ResourceElement = ({resource, isSelected, handleSelect}) => {

    var label = resource.hostname || resource.shortname;

    var status;
    if (resource.available == 'true') {
        status = 'online';
    } else {
        status = 'offline';
    }

    var location = null;
    if (resource.location) {
        //console.log(lookup.countries({name: resource.location.country})[0]);
        // let flag = 'flag-icon flag-icon-' + countries.getCode(resource.location.country);
        // location = <div>Location: <span class={flag}></span> {resource.location.country}</div>;
    }

    return (
         <Element type="resource"
                  element={resource}
                  isSelected={isSelected}
                  handleSelect={handleSelect}
                  status={status}
         >

             <ElementTitle label={resource.name} detail={resource.type} />
             <ElementId id={resource.id} />
             {location}
         </Element>
     );
};

ResourceElement.propTypes = {
    resource: React.PropTypes.object.isRequired,
};

ResourceElement.defaultProps = {
};

const ResourceList = ({resources, selected, handleSelect, options}) => {

    let iconSelected = "check";

    if (selected) {
        if (selected instanceof Array) {
            iconSelected = "check";
        } else {
            selected = [selected];
        }
    }

    if (resources.length == 0) {
        return (
            <div>No Resources</div>
        );
    }

    return (<List>
        {
            resources.map(function(resource) {
                let isSelected = false;
                if (selected) {
                    isSelected = selected.some(function (el) {
                        return el.id === resource.id;
                    });
                }

                return <ResourceElement key={resource.id}
                                        resource={resource}
                                        isSelected={isSelected ? iconSelected : null}
                                        handleSelect={handleSelect}
                                        options={options}
                />;
            })
        }
    </List>);
};

ResourceList.propTypes = {
    resources: React.PropTypes.array.isRequired,
};

ResourceList.defaultProps = {
};

const ResourcesSummary = ({resources}) => {
    let resourcesList = <ul><li>No resources found</li></ul>;

    if (resources.length > 0) {
        resourcesList = <ul>
            {
                resources.map((resource) =>
                    <li key={resource.id}>
                        {resource.hostname}
                        <span>{resource.id}</span>
                    </li>
                )
            }
        </ul>;
    }

    return <div className="summaryList resource">
        <div className="elementIcon summaryIcon resource">
            <Icon name="resource" size="2x"/>
        </div>
        {resourcesList}
    </div>;
};

ResourcesSummary.propTypes = {
    resources: React.PropTypes.array.isRequired
};

ResourcesSummary.defaultProps = {
};

export { ResourceElement, ResourceList, ResourcesSummary };
