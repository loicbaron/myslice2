import React from 'react';
import ReactDOM from 'react-dom';
import PasswordReset from './components/PasswordReset';

var new_hashing = document.getElementById('new_hashing').value;

ReactDOM.render(
        <PasswordReset new_hashing={new_hashing} />,
        document.getElementById('passwordReset')
);
