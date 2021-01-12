<template>
  <div class="personalpage">
    <p class="username"><span>{{ getName }}</span>の投稿</p>
    <Buttons @buttonActive="changeActive" />
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
    name: 'PesonalPage',
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
      changeActive(active) {
        this.isActive = active;
      },
      async getPosts() {
        const path = process.env.VUE_APP_BASE_URL + 'api/getpersonalposts';
        const self = this;
        await this.$api
          .get(path, { params: { user_name: this.$store.state.userName }})
          .then(response => {
            self.$store.commit('changeResult', response.data);
          })
          .catch(error => {
            console.log(error);
          });
      },
    },
    computed: {
      getName() {
        return this.$store.state.userName;
      },
      getResult() {
        return this.$store.getters.getSearchResults;
      },
    },
    async created() {
      await this.getPosts();
    },
  };
</script>

<style lang="scss" scoped>
  .personalpage {
    text-align: center;
    color: #2c3e50;
    background-color: rgb(255, 242, 172);
    border-radius: 6px;
    margin: 0 auto;
    width: 1080px;
  }
  .flex {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    text-align: center;
    margin-top: 20px;
  }
  .username {
    text-align: left;
    font-size: 24px;
    margin-top: 30px;
    margin-bottom: 10px;
    padding-top: 30px;
    padding-left: 30px;
  }
  span {
    font-size: 32px;
  }
</style>
