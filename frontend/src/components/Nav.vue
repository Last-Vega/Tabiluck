<!-- sakuta -->
<template>
  <div id="nav" class="flex">
    <h2 @click="goTop">tabiluck</h2>

    <button @click="openModal">
      <b-icon icon="search"></b-icon>検索
    </button>
    <button class="login" @click="onLogin" v-if="getName === ''">ログイン</button>
    <button class="logout" @click="onLogout" v-if="getName !== ''">ログアウト</button>
    <b-icon icon="person-fill" @click="goPersonal(getName)"></b-icon>

    <div id="search_modal">
      <Modal v-show="showContent" v-on:from-child="closeModal">
        <template slot="send">
          <p>
            キーワード：
            <input v-model="keyword" />
          </p>
          <p>
            旅行日数：
            <select v-model="day">
              <option></option>
              <option v-for="n in 10" :key="n">{{ n }}</option>
            </select>
          </p>
          <p>
            移動手段：
            <select v-model="carChecked">
              <option></option>
              <option>車</option>
              <option>公共交通機関</option>
            </select>
          </p>
          <div class="search_button">
            <button @click="onSearch">検索</button>
          </div>
        </template>
      </Modal>
    </div>
  </div>
</template>

<script>
/* eslint-disable */
import Modal from '@/components/Modal.vue';

export default {
  components: {
    Modal,
  },
  data() {
    return {
      showContent: false,
      keyword: '',
      day: '',
      carChecked: '',
      count: '0',
      showAuth: false,
      showButton: false,
    };
  },
  methods: {
    goTop() {
      if (this.$route.path === '/') {
        const path = process.env.VUE_APP_BASE_URL + 'api/posts';
        this.$api
          .get(path)
          .then(response => {
            this.$store.commit('changeResult', response.data);
          })
          .catch(error => {
            console.log(error);
          });
      } else {
        this.$router.push({ path: '/' });
      }
    },
    openModal() {
      this.showContent = true;
    },
    closeModal() {
      this.showContent = false;
    },
    onSearch() {
      const path = process.env.VUE_APP_BASE_URL + 'api/result';
      const self = this;
      if (this.carChecked === '車') {
        this.carChecked = 0;
      } else if (this.carChecked !== '') {
        this.carChecked = 1;
      }

      this.$api
        .get(path, {
          params: {
            keyword: self.keyword,
            stayed_date: self.day,
            transportation: self.carChecked,
          },
        })
        .then(response => {
          self.$store.commit('changeResult', response.data);
        })
        .catch(error => {
          console.log(error);
        });

      this.keyword = '';
      this.day = '';
      this.carChecked = '';
      this.showContent = false;

      if (this.$route.path !== '/') {
        this.$router.push({ path: '/' });
      }
    },
    onLogin() {
      if (this.$route.path !== '/login') {
        this.$router.push({ path: '/login' });
      }
    },
    onLogout() {
      this.$store.commit('loginUser', '');
      if (this.$route.path !== '/') {
        this.$router.push({ path: '/' });
      }
    },
    goPersonal(userName) {
      if (userName === '') {
        if (this.$route.path !== '/register') {
          this.$router.push({ path: '/register' });
        }
      } else {
        if (this.$route.path !== '/personalpage') {
          this.$router.push({ path: '/personalpage' });
        }
      }
    },
  },
  computed: {
    getName() {
      return this.$store.state.userName;
    },
  },
};
</script>

<style lang='scss' scoped>
#nav {
  border-bottom: 1px solid #000;
  color: #2c3e50;
  margin: 0 auto;
  padding: 10px 180px;
  text-align: center;
  position: relative;
  p {
    margin: 0 0 0 20px;
  }
  a {
    text-decoration: none;
  }
  a.router-link-exact-active {
    color: #2c3e50;
  }
}
.bi-person-fill {
  height: 45px;
  width: 45px;
}
.flex {
  display: flex;
  align-items: center;
}
h2 {
  font-size: 40px;
  margin: 10px auto 10px 0;
}
button {
  appearance: none;
  border: none;
  border-radius: 6px;
  background-color: #bebebe;
  cursor: pointer;
  margin-right: 50px;
  outline: none;
  padding: 8px 16px;
}
.bi-search {
  margin-right: 5px;
}
#search_modal {
  text-align: left;

  p {
    margin-bottom: 20px;
  }
  .search_button {
    text-align: center;
    button {
      margin: 0;
    }
  }
}
.login {
  background-color: rgb(83, 109, 255);
  margin-right: 40px;
  padding: 8px;
  width: 100px;
}
.logout {
  background-color: rgb(255, 155, 40);
  margin-right: 40px;
  padding: 8px;
  width: 100px;
}
</style>
