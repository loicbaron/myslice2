import React from 'react';

class Panel extends React.Component {

    render() {
        return (
            <div>
                {this.props.children}
            </div>
        );
    }
    
}

export default Panel;