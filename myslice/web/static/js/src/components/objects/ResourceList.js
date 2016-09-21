import React from 'react';

import List from '../base/List';
import ResourcesElement from'./Element';

const ResourcesList = ({resources, setCurrent, current}) =>
    <List>
    {
        resources.map(function(resource) {
            return <ResourcesElement key={resource.id} resource={resource} setCurrent={setCurrent} current={current} />;
        }.bind(this))
    }
    </List>;

ResourcesList.propTypes = {
    resources: React.PropTypes.array.isRequired,
    current: React.PropTypes.object,
};

ResourcesList.defaultProps = {
    current: null,
};

export default ResourcesList;
