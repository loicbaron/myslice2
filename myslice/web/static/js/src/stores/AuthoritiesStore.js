var alt = require('../alt');
var actions = require('../actions/AuthoritiesActions');

class AuthoritiesStore {

    constructor() {
        this.authorities = [];
        this.errorMessage = null;

        this.bindListeners({
            updateAuthorities: actions.UPDATE_AUTHORITIES,
        });

    }


    updateAuthorities(authorities) {
        this.authorities = authorities;
    }

}


module.exports = alt.createStore(AuthoritiesStore, 'AuthoritiesStore');

