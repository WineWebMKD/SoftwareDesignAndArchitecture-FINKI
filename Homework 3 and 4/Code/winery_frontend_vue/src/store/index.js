import { createStore } from 'vuex';

export default createStore({
    state: {
        language: 'EN',
    },
    mutations: {
        setLanguage(state, language) {
            state.language = language;
        },
    },
});