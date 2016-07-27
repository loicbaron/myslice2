import React from 'react';

import Element from '../base/Element';
import ElementTitle from '../base/ElementTitle';
import ElementId from '../base/ElementId';
import ElementStatus from '../base/ElementStatus';
import ElementIcon from '../base/ElementIcon';
import DateTime from '../base/DateTime';

const ResourcesRow = ({resource, setCurrent, current}) => {

    var label = resource.hostname || resource.shortname;

    var button = '';
    var status;
    if (resource.available == 'true') {
        status = 'online';
    } else {
        status = 'offline';
    }
    return (
         <Element element={resource} type="resource" setCurrent={setCurrent} current={current}>
             <ElementStatus status={status} />
             <ElementIcon icon="resource" />
             <ElementTitle label={resource.name} detail={resource.type} />
             <ElementId id={resource.id} />
         </Element>
     );
};

ResourcesRow.propTypes = {
    resource: React.PropTypes.object.isRequired,
};

ResourcesRow.defaultProps = {
    current: false,
};

export default ResourcesRow;
