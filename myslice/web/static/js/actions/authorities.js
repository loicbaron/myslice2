/**
 * Authorities Select actions
 */

class AuthoritiesSelectActions {

    fetchAuthorities() {
        axios.get('/api/v1/authorities').then((response) => {
            let s = response.data.result
            console.log(response)
            let options = [{
                label: 'Create new project',
                value: 'pro',
                disabled: true,
                link: this.renderLink()
            }]
            for(let i=0; i<10; i++) {
                options.push({
                    value: s[i].id,
                    label: s[i].name + "<br>" + s[i].id,
                })
            }

            callback(null, {
                options: options,
                complete: true
            });
        });
        // return (dispatch) => {
        //     // we dispatch an event here so we can have "loading" state.
        //     dispatch();
        //     axios.get('/api/v1/authorities', {
        //         }).then(function (response) {
        //             this.updateProject(response.data.result);
        //             console.log(response.data.result);
        //         }.bind(this)).catch(function (response) {
        //             this.errorProject('error');
        //             console.log(response);
        //         }.bind(this));
        //
        //         axios.get('/api/v1/activity?object=PROJECT', {
        //         }).then(function (response) {
        //             this.updateProject(response.data.activity);
        //             console.log(response.data.activity);
        //         }.bind(this)).catch(function (response) {
        //             this.errorProject('error');
        //             console.log(response);
        //         }.bind(this));
        //
        // }
    }

    updateProjectElement(project) {
        return project;
    }

    updateProject(project) {
        return project;
    }

    errorProject(errorMessage) {
        return errorMessage
    }

}

window.AuthoritiesSelectActions = alt.createActions(AuthoritiesSelectActions);