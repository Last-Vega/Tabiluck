<!-- sakuta -->
<template>
  <div class="articles">
    <div class="flex">
      <p class="description">みんなの投稿</p>
      <p class="username">ようこそ、{{ getName }}さん</p>
    </div>
    <Buttons @buttonActive="changeActive" />
    <p class="nohit" v-if="getResult.length === 0">ヒットしませんでした…</p>
    <div class="flex">
      <template v-for="(result, key) in getResult">
        <Article
          :key="key"
          v-if="isActive == result.traveled_flag"
          :title="result.post_name"
          :image_base64="result.image_base64"
          :content="result.content"
          :postID="result.id"
          :countLike="result.count_like"
          @getPosts="getPosts"
        ></Article>
      </template>
    </div>
    <FloatingButton />
  </div>
</template>

<script>
/* eslint-disable */
  import Article from '../components/Article';
  import FloatingButton from '../components/FloatingButton';
  import Buttons from '../components/Buttons';
  export default {
    name: 'Articles',
    components: {
      Article,
      FloatingButton,
      Buttons,
    },
    data() {
      return {
        isActive: 1,
      };
    },
    methods: {
      async getPosts() {
        const path = process.env.VUE_APP_BASE_URL + 'api/posts';
        const self = this;
        await this.$api
          .get(path)
          .then(response => {
            self.$store.commit('changeResult', response.data);
          })
          .catch(error => {
            console.log(error);
          });
      },
      changeActive(active) {
        this.isActive = active;
      },
    },
    async created() {
      await this.getPosts();
    },
    computed: {
      getResult() {
        return this.$store.getters.getSearchResults;
      },
      getName() {
        if (this.$store.state.userName === '') {
          return 'ゲスト';
        } else {
          return this.$store.state.userName;
        }
      },
    },
    mounted() {
      const self = this;
      const path =
        process.env.VUE_APP_BASE_URL + 'api/get-image/post/仙台城.jpeg';
      this.$api
        .get(path)
        .then(res => {
          self.image = res.data;
        })
        .catch(e => console.log(e));
    },
  };
</script>

<style lang="scss" scoped>
  .articles {
    text-align: center;
    color: #2c3e50;
    margin: 0 auto;
    width: 1080px;
  }
  .flex {
    align-items: center;
    display: flex;
    flex-wrap: wrap;
    margin-top: 20px;
    text-align: center;
  }
  .nohit {
    font-size: 24px;
    margin-top: 100px;
  }
  .description {
    text-align: left;
    font-size: 24px;
    margin: 10px 0;
  }
  .username {
    text-align: left;
    font-size: 24px;
    margin: 10px 0 10px auto;
  }
</style>
