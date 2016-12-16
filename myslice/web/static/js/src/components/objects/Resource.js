import React from 'react';

import Title from '../base/Title';
import { List, ListSimple } from '../base/List';
import { Element } from '../base/Element';
import ElementTitle from '../base/ElementTitle';
import ElementId from '../base/ElementId';
import DateTime from '../base/DateTime';

const ResourceElement = ({resource, isSelected, handleSelect}) => {

    var label = resource.hostname || resource.shortname;

    var button = '';
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
                  icon="resource"
                  iconSelected="check"
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

    if ((selected) && (selected instanceof Object)) {
        selected = [selected];
        iconSelected = "arrow";
    }
    if(resources.length==0){
        return (
            <div>No Resources</div>
        );
    }
    return (<List>
        {
            resources.map(function (resource) {
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

export { ResourceElement, ResourceList };
