import React from 'react';

class Panel extends React.Component {

    render() {
        return (
            <div className="col-sm-6">
                { this.props.children }
            </div>
        );
    }
    
}

export default Panel;