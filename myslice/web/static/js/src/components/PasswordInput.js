import React from 'react';

class PasswordInput extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            'class' : '',
            'helperText': ''
        };

        this.updatePassword = this.updatePassword.bind(this);
    }

    validatePassword(password) {
        var re = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,25}$/;
        return re.test(password);
    }

    updatePassword(event) {
        var password = event.target.value;

        if (this.validatePassword(password)) {
            this.setState({
                        'class' : '',
                        'helperText': ''
                        });
            this.props.handleChange(email);
        
        } else {
            this.setState({
                        'class' : 'error',
            });
            // show helper Text if required
            if (this.props.showPattern) {
                this.checkPattern(password);
            }
            console.log('new')
        }
    }

    checkPattern(password){
        if (password.length < 8) {
            this.setState({ 'helperText': 'Must be at least 8 characters long.'});
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

        if (password.length > 25) {
            this.setState({ 'helperText': 'Too long, at most 25 characters.'});
            return;
        }
    }


    render() {
        
        let message = <div>{this.state.helperText}</div>;
        let reavealed = this.props.reavealed ? "text" : "password";

        return (
            <div>
                <input  onChange={this.updatePassword} 
                        className={this.state.class} 
                        placeholder={this.props.placeholder} 
                        type={reavealed}
                        name={this.props.name} />
                {message}
            </div>
        );
    }
}

PasswordInput.propTypes = {
    name: React.PropTypes.string,
    placeholder: React.PropTypes.string,
    showPattern: React.PropTypes.bool,
    reavealed: React.PropTypes.bool
}

PasswordInput.defaultProps = {
    name: 'name',
    placeholder: 'password',
    showPattern: true,
    reavealed: false,
}

export default PasswordInput;