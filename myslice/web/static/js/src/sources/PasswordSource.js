import axios from 'axios';
import actions from '../actions/PasswordActions'

const PasswordSource = () => {
    return {
            onSubmit: {
                remote(state) {
                    return axios.put('/api/v1/password/'+state.hashing,
                        {
                            "password": state.password,
                        });
                },

                success: actions.submitSuccess, // (required)
                error: actions.errorupdatePassword, // (required)

                shouldFetch(state) {
                    return true
                }
            },
            submitEmail: {
                remote(state) {
                    return axios.put('/api/v1/password/',
                        {
                            "email": state.email,
                        });
                },

                success: actions.successEmail, // (required)
                error: actions.errorupdateEmail, // (required)

                shouldFetch(state) {
                    return true
                }
            },
    }
};

export default PasswordSource;
