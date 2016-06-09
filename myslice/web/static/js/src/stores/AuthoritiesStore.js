var alt = require('../alt');
var actions = require('../actions/AuthoritiesActions');
var source = require('../sources/AuthoritiesSource');

class AuthoritiesStore {

    constructor() {
        this.authorities = [];
        this.errorMessage = null;

        this.bindListeners({
            updateAuthorities: actions.UPDATE_AUTHORITIES,
            fetchAuthorities: actions.FETCH_AUTHORITIES,
        });

        this.registerAsync(source);
        
    }

    fetchAuthorities() {

        this.authorities = [];

        if (!this.getInstance().isLoading()) {
            this.getInstance().fetch();
        }

    }

    updateAuthorities(authorities) {
        if (authorities.hasOwnProperty('data')) {
            this.authorities = authorities.data.result;
        } else {
            this.authorities = authorities;
        }
    }

}


module.exports = alt.createStore(AuthoritiesStore, 'AuthoritiesStore');

