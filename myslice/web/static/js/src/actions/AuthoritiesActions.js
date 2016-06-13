import alt from '../alt';

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

export default alt.createActions(AuthoritiesActions);