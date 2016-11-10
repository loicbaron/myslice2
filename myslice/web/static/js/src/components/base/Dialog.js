import React from 'react';

const DialogPanel = ({children}) =>
     <div className="container">
        <div className="row">
            <div className="col-sm-8 col-sm-offset-2">
                <div className="d-panel">
                    {children}
                </div>
            </div>
        </div>
    </div>;

class Dialog extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            closed: false
        };
        this.open = this.open.bind(this);
        this.close = this.close.bind(this);
        this._handleEscKey = this._handleEscKey.bind(this);
        this._handleClick = this._handleClick.bind(this);
    }

    _handleClick(event){
        if (event.target.className == "dialog") {
            this.close();
        }
    }

    _handleEscKey(event){
        if (event.keyCode == 27) {
            this.close();
        }
    }

    open() {
        this.setState({
            closed: false
        });
    }

    close() {
        this.setState({
            closed: true
        });
        this.props.close();
    }

    render() {
        if (!this.props.show) {
            return (
                <div className="dialog" onKeyDown={this._handleEscKey} onClick={this._handleClick} >
                    <div className="dialogClose" onClick={this.close}>
                        <i className="fa fa-close fa-2x fa-fw"></i>
                    </div>
                    {this.props.children}
                </div>
            );
        } else {
            return null;
        }
    }

}

Dialog.propTypes = {
    close: React.PropTypes.func,
};

Dialog.defaultProps = {
};

const DialogHeader = ({children}) => {

    var num = React.Children.count(children);
    if (num >= 2) {
        return (
            <div className="d-header">
                <div className="row">
                    <div className="col-sm-6">
                        {children[0]}
                    </div>
                    <div className="col-sm-6 d-header-right">
                        {children.slice(1)}
                    </div>
                </div>
            </div>
        );
    } else {
        return (
            <div className="d-header">
                <div className="row">
                    <div className="col-sm-12">
                        {children}
                    </div>
                </div>
            </div>
        );
    }

};

const DialogBody = ({children}) =>
            <div className="d-body">
                { children }
            </div>;

const DialogFooter = ({children}) => {

    return (
        <div className="d-footer">
            <div className="row">
                <div className="col-sm-12">
                    {children}
                </div>
            </div>
        </div>
    );

};

export { DialogPanel, Dialog, DialogBody, DialogFooter, DialogHeader };
