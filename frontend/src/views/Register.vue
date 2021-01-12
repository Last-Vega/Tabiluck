<!-- sakuta -->
<template>
  <div class="register">
    <h3>新規登録</h3>
    <div class="register_form">
      <div class="flex">
        <p>名前</p>
        <input type="text" v-model="userName" />
      </div>
      <div class="flex">
        <p>メールアドレス</p>
        <input type="text" v-model="mailAdress" />
      </div>
      <div class="flex">
        <p>パスワード</p>
        <input type="password" v-model="password" />
      </div>
      <div class="flex">
        <p>再パスワード</p>
        <input type="password" v-model="rePassword" />
      </div>

      <button class="register-button" @click="register">登録</button>
    </div>

    <div class="flex pagelink">
      <router-link to="/">
        <p>トップへ戻る</p>
      </router-link>
      <router-link to="/login">
        <p>ログイン画面へ</p>
      </router-link>
    </div>
  </div>
</template>

<script>

export default {
  name: 'Register',
  data () {
    return {
      userName: '',
      mailAdress: '',
      password: '',
      rePassword: ''
    }
  },
  methods: {
    async register () {
      if (this.userName === '') {
        alert('ユーザネームを入力してください')
        return
      }
      if (this.mailAdress === '') {
        alert('メールアドレスを入力してください')
        return
      }
      if (this.password === '') {
        alert('パスワードを入力してください')
        return
      }
      if (this.rePassword === '') {
        alert('パスワードを再度入力してください')
        return
      }
      if (this.password !== this.rePassword) {
        this.password = ''
        this.rePassword = ''
        alert('パスワードが一致しません')
        return
      }

      const path = process.env.VUE_APP_BASE_URL + 'api/registration'
      const self = this
      // パスワードのハッシュ化
      const uint8 = new TextEncoder().encode(this.password)
      const digest = await crypto.subtle.digest('SHA-256', uint8)
      this.password = Array.from(new Uint8Array(digest))
        .map(v => v.toString(16).padStart(2, '0'))
        .join('')

      const params = new URLSearchParams()
      params.append('name', self.userName)
      params.append('email', self.mailAdress)
      params.append('password', self.password)

      this.$api
        .post(path, params)
        .catch(error => {
          console.log(error)
        })

      this.$router.push('/login')
    }
  }
}
</script>

<style lang="scss" scoped>
.register {
  text-align: center;
  color: #2c3e50;
  margin: 50px auto;
  width: 1080px;
}
.register_form {
  border: 1px solid #000;
  border-radius: 12px;
  margin: 0 auto 20px;
  text-align: center;
  padding: 20px;
  width: 400px;
}
a {
  color: inherit;
  &:hover {
    color: red;
  }
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
.register-button {
  background-color: rgb(255, 155, 40);
  padding: 8px 24px;
  margin-top: 20px;
}
</style>
