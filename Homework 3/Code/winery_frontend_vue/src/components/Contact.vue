<template>
  <div class="outer-block-contact">
    <h2 class="form-title">PLEASE FILL OUT THE FORM BELOW TO SEND US AN E-MAIL</h2>
    <form class="inner-block-contact" @submit.prevent="submitForm">
      <div class="form-field">
        <label for="name">Name:</label>
        <input type="text" id="name" name="name" v-model="formData.name">
      </div>

      <div class="form-field">
        <label for="email">E-mail:</label>
        <input type="email" id="email" name="email" v-model="formData.email">
      </div>

      <div class="form-field">
        <label for="subject">Subject:</label>
        <input type="text" id="subject" name="subject" v-model="formData.subject">
      </div>

      <div class="form-field form-message">
        <label for="message">Message:</label>
        <textarea id="message" name="message" v-model="formData.message"></textarea>
      </div>

      <button type="submit" class="submit-button">SUBMIT</button>
    </form>
  </div>
</template>

<script>
export default {
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
    submitForm() {
      // You can perform form validation here before sending the data
      // For example, check if the required fields are filled

      // Assuming you are using axios for making HTTP requests
      // Replace 'http://localhost:yourport/yourendpoint' with your backend URL
      console.log("WOOT")
      // axios.post('http://localhost:yourport/yourendpoint', this.formData)
      //     .then(response => {
      //       console.log('Form submitted successfully!', response);
      //       // Handle success, show a success message, or redirect the user
      //     })
      //     .catch(error => {
      //       console.error('Error submitting form:', error);
      //       // Handle error, show an error message
      //     });
    }
  }
};
</script>

<style>
/* Your existing CSS styles can be placed here */
</style>
