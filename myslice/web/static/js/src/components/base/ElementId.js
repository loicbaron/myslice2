import React from 'react';

class ElementId extends React.Component {

    render() {

        return (
            <h4 className="elementId">
                {this.props.id}
            </h4>
        );

    }
}

export default ElementId;