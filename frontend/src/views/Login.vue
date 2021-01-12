<!-- sakuta -->
<template>
  <div class="login">
    <h3>ログイン</h3>
    <div class="login_form">
      <div class="flex">
        <p>メールアドレス</p>
        <input type="text" v-model="mailAdress" />
      </div>
      <div class="flex">
        <p>パスワード</p>
        <input type="password" v-model="password" />
      </div>

      <button class="login-button" @click="login">ログイン</button>
    </div>

    <div class="flex pagelink">
      <router-link to="/">
        <p>トップへ戻る</p>
      </router-link>
      <router-link to="/register">
        <p>登録画面へ</p>
      </router-link>
    </div>
  </div>
</template>

<script>
/* eslint-disable */
export default {
  name: 'Login',
  data() {
    return {
      mailAdress: '',
      password: '',
    };
  },
  methods: {
    async login() {
      if (this.mailAdress === '') {
        alert('メールアドレスを入力してください');
        return;
      }
      if (this.password === '') {
        alert('パスワードを入力してください');
        return;
      }

      const path = process.env.VUE_APP_BASE_URL + 'api/login';
      const self = this;
      // パスワードのハッシュ化
      const uint8 = new TextEncoder().encode(this.password);
      const digest = await crypto.subtle.digest('SHA-256', uint8);
      const hashPassword = Array.from(new Uint8Array(digest))
        .map(v => v.toString(16).padStart(2, '0'))
        .join('');

      let params = new URLSearchParams();
      params.append('email', self.mailAdress);
      params.append('password', hashPassword);

      this.$api
        .post(path, params)
        .then(response => {
          if (response.data === 'permission denied') {
            alert('メールアドレスかパスワードが間違っています。');
            self.password = '';
          } else {
            self.$store.commit('loginUser', response.data);
            this.$router.push('/personalpage');
          }
        })
        .catch(error => {
          console.log(error);
        });
    },
  },
};
</script>

<style lang="scss" scoped>
.login {
  text-align: center;
  color: #2c3e50;
  margin: 50px auto;
  width: 1080px;
}
.login_form {
  border: 1px solid #000;
  border-radius: 12px;
  margin: 0 auto 20px;
  text-align: center;
  padding: 20px;
  width: 400px;
}
.flex {
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: left;
  margin: 20px 0;

  p {
    margin: 0;
    width: 130px;
  }
}
a {
  color: inherit;
  &:hover {
    color: red;
  }
}
.pagelink {
  margin: 0 auto;
  width: 400px;
  justify-content: space-between;
  p {
    width: auto;
  }
}
button {
  border: none;
  cursor: pointer;
  outline: none;
  padding: 8px 16px;
  appearance: none;
  border-radius: 6px;
}
.login-button {
  background-color: rgb(83, 109, 255);
  margin-top: 20px;
}
</style>
