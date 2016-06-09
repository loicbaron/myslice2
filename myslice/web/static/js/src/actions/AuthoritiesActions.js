var alt = require('../alt');
var axios = require('axios');

class AuthoritiesActions {

    fetchAuthorities() {
        return true;
    }

    updateAuthorities(authorities) {
        return authorities;
    }

    errorAuthorities(errorMessage) {
        return errorMessage
    }

}

module.exports = alt.createActions(AuthoritiesActions);