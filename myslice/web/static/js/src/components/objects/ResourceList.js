import React from 'react';

import List from '../base/List';
import ResourceElement from './ResourceElement';

const ResourceList = ({resources, selected, handleSelect}) =>
    <List>
    {
        resources.map(function(resource) {
            let isSelected = selected.some(function(el) {
                return el.id === resource.id;
            });

            return <ResourceElement key={resource.id} isSelected={isSelected} resource={resource} handleSelect={handleSelect} />;
        }.bind(this))
    }
    </List>;

ResourceList.propTypes = {
    resources: React.PropTypes.array.isRequired,
};

ResourceList.defaultProps = {
};

export default ResourceList;
