import React from 'react';

class PanelHeader extends React.Component {
    render() {
        return (
                <div className="p-header">
                    <div className="container-fluid">
                        <div class="row">
                            {this.props.children}
                        </div>
                    </div>
                </div>
        );
    }
}

export default PanelHeader;