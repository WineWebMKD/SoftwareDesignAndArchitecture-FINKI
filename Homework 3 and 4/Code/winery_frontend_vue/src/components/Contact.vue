<template>
  <div class="outer-block-contact">
    <h2 class="form-title">{{ language === 'EN' ? 'PLEASE FILL OUT THE FORM BELOW TO SEND US AN E-MAIL'
        : 'ВЕ МОЛИМЕ ПОПОЛНЕТЕ ГО ФОРМУЛАРОТ ПОДОЛУ ЗА ДА НИ ПРАТИТЕ Е-ПОШТА' }}</h2>
    <form class="inner-block-contact" @submit.prevent="submitForm">
      <div class="form-field">
        <label for="name">{{ language === 'EN' ? 'Name:' : 'Име:' }}</label>
        <input type="text" id="name" name="name" v-model="formData.name" required>
      </div>

      <div class="form-field">
        <label for="email">{{ language === 'EN' ? 'E-mail:' : 'Е-пошта:' }}</label>
        <input type="email" id="email" name="email" v-model="formData.email" required>
      </div>

      <div class="form-field">
        <label for="subject">{{ language === 'EN' ? 'Subject:' : 'Предмет:' }}</label>
        <input type="text" id="subject" name="subject" v-model="formData.subject" required>
      </div>

      <div class="form-field form-message">
        <label for="message">{{ language === 'EN' ? 'Message:' : 'Порака:' }}</label>
        <textarea id="message" name="message" v-model="formData.message" required></textarea>
      </div>
      <button type="submit" class="submit-button">{{ language === 'EN' ? 'SUBMIT' : 'ПОДНЕСЕТЕ' }}</button>
    </form>
  </div>
  <pop-up v-if="messagePopup" :message="messagePopup.message" :onClose="messagePopup.onClose">
    <button class="pop-buttons" @click="closeMessagePopup">OK</button>
  </pop-up>
</template>

<script>
import axios from 'axios';
import {useStore} from "vuex";
import {computed} from "vue";
import PopUp from "@/components/PopUp.vue";
export default {
  components: {PopUp},
  setup() {
    const store = useStore();
    const language = computed(() => store.state.language);
    return {
      language
    };
  },
  data() {
    return {
      formData: {
        name: '',
        email: '',
        subject: '',
        message: ''
      },
      messagePopup: null
    };
  },
  methods: {
    async submitForm() {
      try {
        // Send email
        await axios.post('http://127.0.0.1:8000/submit-form', this.formData);
        this.resetForm();
        // Show success message
        let message = this.language === 'EN' ? 'Message sent successfully!' : 'Пораката е успешно испратена!';
        this.showMessagePopup(message);
      } catch (error) {
        console.error('Error sending email:', error);
        // Show error message
        let message = this.language === 'EN' ? 'Error while sending message!' : 'Проблем при испраќање на пораката!';
        this.showMessagePopup(message);
      }
    },
    resetForm() {
      this.formData = {
        name: '',
        email: '',
        subject: '',
        message: ''
      };
    },
    showMessagePopup(message) {
      this.messagePopup = {
        message: message,
        onClose: this.closeMessagePopup
      };
    },
    closeMessagePopup() {
      this.messagePopup = null;
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
  width: 100%;
  height: 20%;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.form-title {
  color: #7D1310;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1em;
  text-align: center;
  font-weight: bold;
}
.form-field {
  background-color: #B18B6A;
  box-shadow: 0 8px 10px rgba(0, 0, 0, 0.6);
  color: white;
  width: 90%;
  height: 10%;
  border-radius: 10px;
  font-size: 14px;
  margin: 1%;
  padding: 3%;
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
  width: 150px;
  height: 30px;
  border-radius: 100px;
  margin-top: 20px;
  cursor: pointer;
}

.submit-button:hover {
  background-color: #4E0D0A;
}
input {
  background: #B18B6A;
  height: 25px;
  width: 300px;
  border: none;
}
textarea {
  background: #B18B6A;
  width: 500px;
  height: 130px;
  border: none;
}
</style>
