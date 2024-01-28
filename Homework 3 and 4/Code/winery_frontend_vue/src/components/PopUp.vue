<template>
  <div class="popup">
    <p>{{ message }}</p>
    <slot></slot>
  </div>
</template>

<script>
export default {
  props: {
    message: String
  }
};
</script>

<style>
.popup {
  background-color: white;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.5);
  color: #7D1310;
  position: fixed;
  border-radius:  10px;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 20px;
  z-index: 999;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.pop-buttons {
  background-color: #8d0e0e;
  color: #ffffff;
  width: 20%;
  height: 20%;
  border-radius: 100px;
  cursor: pointer;
}
</style>