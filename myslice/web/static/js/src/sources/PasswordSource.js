import axios from 'axios';
import actions from '../actions/PasswordActions'

const PasswordSource = () => {
    return {
            submitEmail: {
                remote(state) {
                    return axios.post('/api/v1/password/',
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
