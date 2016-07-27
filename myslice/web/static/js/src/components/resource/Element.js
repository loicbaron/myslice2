import React from 'react';

import Element from './base/Element';
import ElementTitle from './base/ElementTitle';
import ElementId from './base/ElementId';
import ElementStatus from './base/ElementStatus';
import ElementIcon from './base/ElementIcon';
import DateTime from './base/DateTime';

const ResourcesRow = ({resource}) => {

    var label = resource.hostname || resource.shortname;

    var button = '';

    return (
         <Element element={resource} type="project">
             <ElementStatus status={resource.status} />
             <ElementIcon icon="resource" />
             <ElementTitle label={label} detail={resource.hostname} />
             <ElementId id={resource.id} />
         </Element>
     );
}

ResourcesRow.propTypes = {
    resource: React.PropTypes.object.isRequired,
};

ResourcesRow.defaultProps = {
    select: false,
};

export default ResourcesRow;
