var alt = require('../alt');
var axios = require('axios');

class AuthoritiesActions {

    fetchAuthorities() {
        return (dispatch) => {
            // we dispatch an event here so we can have "loading" state.
            dispatch();
            axios.get('/api/v1/authorities').then(function (response) {
                this.updateAuthorities(response.data.result);
            }.bind(this)).catch(function (response) {
                console.log(response);
                this.updateAuthorities('error');
            }.bind(this));

        }
       
    }

    updateAuthorities(authorities) {
        return authorities;
    }

    errorAuthorities(errorMessage) {
        return errorMessage
    }

}

module.exports = alt.createActions(AuthoritiesActions);