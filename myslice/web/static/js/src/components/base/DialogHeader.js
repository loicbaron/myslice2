import React from 'react';

class DialogHeader extends React.Component {
    render() {
        var num = React.Children.count(this.props.children);
        if (num >= 2) {
            return (
                <div className="d-header">
                    <div className="row">
                        <div className="col-sm-6">
                            {this.props.children[0]}
                        </div>
                        <div className="col-sm-6 d-header-right">
                            {this.props.children.slice(1)}
                        </div>
                    </div>
                </div>
            );
        } else {
            return (
                <div className="d-header">
                    <div className="row">
                        <div className="col-sm-12">
                            {this.props.children}
                        </div>
                    </div>
                </div>
            );
        }
    }
}

export default DialogHeader;