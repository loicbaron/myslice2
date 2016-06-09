var alt = require('../alt');
var actions = require('../actions/Authorities');
var source = require('../sources/Authoritites');

class AuthoritiesStore {

    constructor() {
        this.authorities = [];
        this.errorMessage = null;

        this.bindListeners({
            updateAuthorities: actions.UPDATE_AUTHORITIES,
        });

        this.registerAsync(source);
    }


    updateAuthorities(authorities) {
        this.authorities = authorities;
    }

}


module.exports = alt.createStore(AuthoritiesStore, 'AuthoritiesStore');

