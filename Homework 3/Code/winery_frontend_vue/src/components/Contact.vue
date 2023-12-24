<template>
  <div class="outer-block-contact">
    <h2 class="form-title">{{ language === 'EN' ? 'PLEASE FILL OUT THE FORM BELOW TO SEND US AN E-MAIL'
        : 'ВЕ МОЛИМЕ ПОПОЛНЕТЕ ГО ФОРМУЛАРОТ ПОДОЛУ ЗА ДА НИ ПРАТИТЕ Е-ПОШТА' }}</h2>
    <form class="inner-block-contact" @submit.prevent="submitForm">
      <div class="form-field">
        <label for="name">{{ language === 'EN' ? 'Name:' : 'Име:' }}</label>
        <input type="text" id="name" name="name" v-model="formData.name">
      </div>

      <div class="form-field">
        <label for="email">{{ language === 'EN' ? 'E-mail:' : 'Е-пошта:' }}</label>
        <input type="email" id="email" name="email" v-model="formData.email">
      </div>

      <div class="form-field">
        <label for="subject">{{ language === 'EN' ? 'Subject:' : 'Предмет:' }}</label>
        <input type="text" id="subject" name="subject" v-model="formData.subject">
      </div>

      <div class="form-field form-message">
        <label for="message">{{ language === 'EN' ? 'Message:' : 'Порака:' }}</label>
        <textarea id="message" name="message" v-model="formData.message"></textarea>
      </div>

      <button type="submit" class="submit-button">{{ language === 'EN' ? 'SUBMIT' : 'ПОДНЕСЕТЕ' }}</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';
import {useStore} from "vuex";
import {computed} from "vue";
export default {
  setup() {
    const store = useStore();
    const language = computed(() => store.state.language);

    return {
      language,
    };
  },
  data() {
    return {
      formData: {
        name: '',
        email: '',
        subject: '',
        message: ''
      }
    };
  },
  methods: {
    async submitForm() {
      try {
        // Send email
        await axios.post('http://127.0.0.1:8000/submit-form', this.formData);

        // Handle success (e.g., show a success message)
        console.log('Email sent successfully!');
      } catch (error) {
        // Handle error (e.g., show an error message)
        console.error('Error sending email:', error);
      }
    }
  }
};
</script>

<style>
/* Your existing CSS styles can be placed here */
</style>
