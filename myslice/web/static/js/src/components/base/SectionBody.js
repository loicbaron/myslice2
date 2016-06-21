import React from 'react';

class SectionBody extends React.Component {
    render() {
        return (
                <div className="s-body">
                    <div className="row">
                        <div className="col-md-12">
                            { this.props.children }
                        </div>
                    </div>
                </div>
        );
    }
}

export default SectionBody;