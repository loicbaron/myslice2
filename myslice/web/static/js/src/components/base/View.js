import React from 'react';

class View extends React.Component {

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

export default View;