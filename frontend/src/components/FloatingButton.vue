<!-- sakuta -->
<template>
  <b-icon @click="goPostForm(getUserName)" icon="plus-circle-fill"></b-icon>
</template>

<script>
/* eslint-disable */
export default {
  methods: {
    goPostForm(userName) {
      if (userName === '') {
        this.$router.push({ path: '/login' });
      } else {
        this.$router.push({ path: '/post' });
      }
    },
  },
  computed: {
    getUserName() {
      return this.$store.state.userName;
    },
  },
};
</script>

<style lang="scss" scoped>
.bi-plus-circle-fill {
  color: #007bff;
  position: fixed;
  right: 50px;
  bottom: 50px;
  height: 50px;
  width: 50px;
}
</style>
