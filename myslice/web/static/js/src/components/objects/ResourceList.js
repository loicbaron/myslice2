import React from 'react';

import List from '../base/List';
import ResourceElement from './ResourceElement';

const ResourceList = ({resources, setCurrent, current}) =>
    <List>
    {
        resources.map(function(resource) {
            return <ResourceElement key={resource.id} resource={resource} setCurrent={setCurrent} current={current} />;
        }.bind(this))
    }
    </List>;

ResourceList.propTypes = {
    resources: React.PropTypes.array.isRequired,
    current: React.PropTypes.object,
};

ResourceList.defaultProps = {
    current: null,
};

export default ResourceList;
