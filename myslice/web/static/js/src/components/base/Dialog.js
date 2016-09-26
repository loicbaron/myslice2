import React from 'react';

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

export default Dialog;
