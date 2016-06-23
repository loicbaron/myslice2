import React from 'react';

import List from './base/List';
import SlicesRow from'./SlicesRow';

class SlicesList extends React.Component {

    render() {
        return (
            <List>
            {
                this.props.slices.map(function(slice) {
                    return <SlicesRow key={slice.id} slice={slice} setCurrent={this.props.setCurrent} current={this.props.current} />;
                }.bind(this))
            }
            </List>
        );
    }
}

SlicesList.propTypes = {
    slices: React.PropTypes.array.isRequired,
    current: React.PropTypes.object,
    setCurrent: React.PropTypes.func
};

SlicesList.defaultProps = {
    current: null,
    setCurrent: null
};

export default SlicesList;