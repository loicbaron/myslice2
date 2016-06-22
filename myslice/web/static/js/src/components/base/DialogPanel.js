import React from 'react';

class DialogPanel extends React.Component {

    render() {
        return (
            <div className="container">
                <div className="row">
                    <div className="col-sm-8 col-sm-offset-2">
                        <div className="d-panel">
                            {this.props.children}
                        </div>
                    </div>
                </div>
            </div>
        );
    }

}

export default DialogPanel;