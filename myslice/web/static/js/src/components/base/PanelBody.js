import React from 'react';

class PanelBody extends React.Component {
    render() {
        return (
                <div className="p-body">
                    <div className="container-fluid">
                        <div className="row">
                            <div className="col-md-12">
                                { this.props.children }
                            </div>
                        </div>
                    </div>
                </div>
        );
    }
}

export default PanelBody;