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
        this.resetForm();
        // Show success message (you can replace this with a more styled notification)
        alert(this.language === 'EN' ? 'Message sent successfully!' : 'Пораката е успешно испратена!');
      } catch (error) {
        // Handle error (e.g., show an error message)
        console.error('Error sending email:', error);
        alert(this.language === 'EN' ? 'Error while sending message!' : 'Проблем при испраќање на пораката!');
      }
    },
    resetForm() {
      this.formData = {
        name: '',
        email: '',
        subject: '',
        message: ''
      };
    }
  }
};
</script>

<style scoped>
.outer-block-contact{
  background-color: #CFAA87;
  width: 50%;
  height: 100%;
  margin: 0 auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
}
.inner-block-contact {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  height: 20%;
}
.form-title {
  display: flex;
  justify-content: center; /* Center horizontally */
  align-items: center;
  color: #7D1310;
  font-size: 1em;
  text-align: center;
  font-weight: bold;
}
.form-field {
  background-color: #B18B6A;
  border-radius: 10px;
  color: white;
  font-size: 14px;
  margin: 1%;
  padding: 3%;
  width: 90%;
  height: 10%;
  display: flex;
  align-items: center;
}

.form-field label {
  margin-right: 10px;
}

.form-message {
  height: 150px;
}

.submit-button {
  background-color: #7D1310;
  color: white;
  border-radius: 100px;
  width: 150px;
  height: 30px;
  margin-top: 20px;
  cursor: pointer;
}

.submit-button:hover {
  background-color: #4E0D0A; /* Change the color on hover if desired */
}
input {
  background: #B18B6A;
  border: none;
  height: 25px;
  width: 300px;
}
textarea{
  background: #B18B6A;
  border: none;
  width: 500px;
  height: 130px;
}
</style>
