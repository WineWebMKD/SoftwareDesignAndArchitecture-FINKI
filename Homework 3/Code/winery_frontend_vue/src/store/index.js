import { createStore } from 'vuex';

export default createStore({
    state: {
        language: 'EN',
    },
    mutations: {
        setLanguage(state, language) {
            // Update the language based on the provided parameter
            state.language = language;
        },
    },
});