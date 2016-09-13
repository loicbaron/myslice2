import alt from '../alt';
import actions from '../actions/AuthoritiesActions';
import source from '../sources/AuthoritiesSource';

class AuthoritiesStore {

    constructor() {
        this.authorities = [];
        this.errorMessage = null;

        this.bindListeners({
            updateAuthorities: actions.UPDATE_AUTHORITIES,
            fetchAuthorities: actions.FETCH_AUTHORITIES,
            errorAuthorities: actions.ERROR_AUTHORITIES,
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
    errorAuthorities(errorMessage) {
        console.log(errorMessage);
    } 

}


export default alt.createStore(AuthoritiesStore, 'AuthoritiesStore');

