import React from 'react';

class SectionHeader extends React.Component {
    render() {
        var num = React.Children.count(this.props.children);
        if (num >= 2) {
            return (
                <div className="s-header">
                    <div className="row">
                        <div className="col-sm-6">
                            {this.props.children[0]}
                        </div>
                        <div className="col-sm-6 s-header-right">
                            {this.props.children.slice(1)}
                        </div>
                    </div>
                </div>
            );
        } else {
            return (
                <div className="s-header">
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

export default SectionHeader;