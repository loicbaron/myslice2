import React from 'react';

import store from '../stores/SlicesStore';
import actions from '../actions/SlicesActions';

import List from './base/List';
import SlicesRow from'./SlicesRow';

class SlicesList extends React.Component {

    constructor(props) {
        super(props);
        this.state = store.getState();
        this.onChange = this.onChange.bind(this);
    }

    componentDidMount() {
        store.listen(this.onChange);

        actions.fetchSlices({
                belongTo: this.props.belongTo
        });


    }

    componentWillUnmount() {
        store.unlisten(this.onChange);
    }

    onChange(state) {
        this.setState(state);
    }

    render() {
        return (
            <List>
            {
                this.state.slices.map(function(slice) {
                    return <SlicesRow key={slice.id} slice={slice} select={this.props.select} />;
                }.bind(this))
            }
            </List>
        );
    }
}

SlicesList.propTypes = {
    belongTo: React.PropTypes.object,
    select: React.PropTypes.bool
};

SlicesList.defaultProps = {
    belongTo: { type: null, id: null},
    select: false
};

export default SlicesList;