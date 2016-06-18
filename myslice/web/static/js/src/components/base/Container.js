import React from 'react';

class Container extends React.Component {

    render() {
        return (
            <div className="container-fluid">
                <div className="row">
                {this.props.children}
                </div>
            </div>
        );
    }

}

export default Container;