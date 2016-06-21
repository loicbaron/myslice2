import React from 'react';

class PanelHeader extends React.Component {
    render() {
        var num = React.Children.count(this.props.children);
        if (num >= 2) {
            return (
                <div className="p-header">
                    <div className="container-fluid">
                        <div className="row">
                            <div className="col-sm-6">
                                {this.props.children[0]}
                            </div>
                            <div className="col-sm-6 p-header-right">
                                {this.props.children.slice(1)}
                            </div>
                        </div>
                    </div>
                </div>
            );
        } else {
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
}

export default PanelHeader;