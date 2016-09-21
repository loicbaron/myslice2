import React from 'react';

import Element from '../base/Element';
import ElementTitle from '../base/ElementTitle';
import ElementId from '../base/ElementId';
import ElementStatus from '../base/ElementStatus';
import ElementIcon from '../base/ElementIcon';
import DateTime from '../base/DateTime';

const ResourceElement = ({resource, setCurrent, current}) => {

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
         <Element element={resource} type="resource" setCurrent={setCurrent} current={current}>
             <ElementStatus status={status} />
             <ElementIcon icon="resource" />
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
    current: false,
};

export default ResourceElement;
