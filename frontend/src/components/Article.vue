<!-- sakuta -->
<template>
  <div class="article">
    <div class="flex header">
      <p class="title" @click="detailpage">{{ title }}</p>
      <b-icon icon="person-fill"></b-icon>
    </div>
    <img :src="image_base64" :alt="'旅行「' + title + '」の写真'" />
    <p class="content">{{ content }}</p>
    <div class="flex like">
      <button @click="clickLike" class="like-button">
        <b-icon icon="heart-fill" variant="danger"></b-icon>
      </button>
      <p class="like_num">{{ countLike }}</p>
    </div>
  </div>
</template>

<script>
/* eslint-disable */
  export default {
    props: {
      title: {
        type: String,
        default: 'タイトル',
      },
      image_base64: {
        type: String,
        default:
          'https://atta.ai/media/jp/wp-content/uploads/2019/09/591-itsukushima_0.jpg',
      },
      content: {
        type: String,
        default: '',
      },
      url: {
        type: String,
      },
      postID: {
        type: Number,
      },
      countLike: {
        type: Number,
      },
    },
    methods: {
      detailpage() {
        this.$router.push({
          path: `detail/${this.postID}`,
        });
      },
      clickLike() {
        const login_name = this.$store.getters.getUserName;

        // loginしてなかったらいいねできない
        if (login_name === '') {
          alert('いいねをするにはログインする必要があります。');
          return;
        }

        const self = this;
        const path = process.env.VUE_APP_BASE_URL + 'api/toggleLike';
        let params = new URLSearchParams();
        params.append('post_id', self.postID);
        params.append('liker_name', login_name);

        this.$api
          .post(path, params)
          .then(response => {
            console.log(response.data);
            self.$emit('getPosts');
          })
          .catch(error => console.log(error));
      },
    },
  };
</script>

<style lang="scss" scoped>
  .article {
    color: #2c3e50;
    border: 1px solid #aaa;
    border-radius: 0.3em;
    background-color: #fff;
    width: calc(33.33333% - 40px);
    margin: 20px;

    .flex {
      display: flex;
      align-items: center;
    }

    .header {
      .title {
        margin: 5px auto 5px 10px;
        font-size: 20px;
      }

      .bi-person-fill {
        height: 30px;
        width: 30px;
      }
    }

    img {
      width: 100%;
      height: 240px;
      object-fit: contain;
    }

    .content {
      text-align: left;
      margin: 10px;
      padding: 0;
    }

    .like {
      margin-right: 10px;

      .like-button {
        margin-left: auto;
        margin-right: 5px;
        border: none;
        background: none;
        font-size: 20px;

        &:hover {
          transform: scale(1.5);
        }

        &:focus {
          outline: none;
        }
      }

      .like_num {
        margin: 0;
        font-size: 20px;
      }
    }
  }
</style>
