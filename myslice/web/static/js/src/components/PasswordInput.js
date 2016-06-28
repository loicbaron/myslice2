import React from 'react';

class PasswordInput extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            'class' : '',
            'helperText': '',
        };

        this.updatePassword = this.updatePassword.bind(this);
    }

    validatePassword(password) {
        //Minimum 8 characters at least 1 Uppercase Alphabet, 1 Lowercase Alphabet, 1 Number
        //Special Character is allowed but not required
        var re = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d$@$!%*?&]{8,25}/;
        return re.test(password);
    }

    updatePassword(event) {
        var password = event.target.value;

        if (this.validatePassword(password)) {
            this.setState({
                        'class' : 'correct',
                        'helperText': '',
                        });
            this.props.checkedPassword(password);
        
        } else {
            this.setState({
                        'class' : 'error',
            });
            // show helper Text if required
            if (this.props.showPattern) {
                this.checkPattern(password);
            }
        }
    }

    checkPattern(password){
        if (password.length < 8) {
            this.setState({ 'helperText': 'Must be at least 8 characters long.'});
            return;
        }

        if (password.length > 25) {
            this.setState({ 'helperText': 'Too long, at most 25 characters.'});
            return;
        }
        
        let reLow = /^(?=.*[a-z]).+$/;
        if (!reLow.test(password)) {
            this.setState({ 'helperText': 'Must contain an lowercase letter.'});
            return;
        }
        
        let reUp = /^(?=.*[A-Z]).+$/;
        if (!reUp.test(password)) {
            this.setState({ 'helperText': 'Must contain an Uppercase letter.'});
            return;
        }
        
        let reNum = /^(?=.*[0-9]).+$/;
        if (!reNum.test(password)) {
            this.setState({ 'helperText': 'Must contain a number.'});
            return;
        }


    }

    render() {
        let reavealed = this.props.reavealed ? "text" : "password";

        let message = (<div></div>);
        if (this.state.helperText) {
            message = (<span className="helpBlock">{this.state.helperText}</span>);
        }

        let icon = (this.props.correct) ? <i className="fa fa-check inputIcon"></i>: <i></i>;

        return (
            <div className="settings-group resetPassword">
                <span className="settings-span">{this.props.description}</span>
                <input  onChange={this.updatePassword} 
                        className={this.state.class} 
                        placeholder={this.props.placeholder} 
                        type={reavealed}
                        name={this.props.name}
                        />
                {icon}
            {message}
            </div>
        );
    }
}

PasswordInput.propTypes = {
    name: React.PropTypes.string,
    placeholder: React.PropTypes.string,
    showPattern: React.PropTypes.bool,
    reavealed: React.PropTypes.bool,
    checkedPassword: React.PropTypes.func
}

PasswordInput.defaultProps = {
    name: 'name',
    placeholder: 'password',
    showPattern: true,
    reavealed: false,
}

export default PasswordInput;