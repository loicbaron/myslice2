import React from 'react';

import List from './base/List';
import ResourcesRow from'./ResourcesRow';

class ResourcesList extends React.Component {

    render() {
        return (
            <List>
            {
                this.props.resources.map(function(resource) {
                    return <ResourcesRow key={resource.id} resource={resource} setCurrent={this.props.setCurrent} current={this.props.current} />;
                }.bind(this))
            }
            </List>
        );
    }
}

ResourcesList.propTypes = {
    resources: React.PropTypes.array.isRequired,
    current: React.PropTypes.object,
};

ResourcesList.defaultProps = {
    current: null,
};

export default ResourcesList;
