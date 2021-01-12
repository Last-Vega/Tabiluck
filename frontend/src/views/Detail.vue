<!-- nakano? -->
<template>
  <div class="detail">
    <div class="schedule">
      <div class="schedule-container">
        <div class="plan">
          <div class="trip-title">
            <h3>Title: {{ results.post_information.post_name }}</h3>
            <p>created by: {{ results.post_information.user_name }}</p>
            <p>{{ results.post_information.content }}</p>
          </div>
          <table class="vue-tbl">
            <thead>
              <tr>
                <th>Dates</th>
                <th>Location</th>
                <th>Transportation</th>
                <th>Memo</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(schedule, i) in results.schedule_information" :key="i">
                <td>
                  {{ schedule.start_year }}年{{ ('0' + schedule.start_month).slice(-2) }}月{{
                  ('0' + schedule.start_date).slice(-2)
                  }}日 {{ ('00' + schedule.start_hour).slice(-2) }}:{{ ('00' + schedule.start_min).slice(-2) }}〜{{
                  ('00' + schedule.end_hour).slice(-2)
                  }}:{{ ('00' + schedule.end_min).slice(-2) }}
                </td>
                <td>{{ schedule.title }}</td>
                <td>{{ schedule.transportation }}</td>
                <td>{{ schedule.memo }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div id="gmap">
          <img :src="results.post_information.image_base64" alt="写真" />
          <GmapMap
            ref="mapRef"
            :center="getCenter()"
            :zoom="9"
            :options="{ streetViewControl: false }"
            map-type-id="terrain"
            style="width: 470px; height: 300px"
          >
            <GmapMarker
              :key="index"
              v-for="(schedule, index) in results.schedule_information"
              :position="{ lat: schedule.latitude, lng: schedule.longitude }"
              :clickable="true"
              :draggable="true"
              :icon="{fillColor: '#ff8c00', fillOpacity: 0.8, path: google.maps.SymbolPath.CIRCLE, scale: 16, strokeColor: '#ff8c00',strokeWeight: 1.0}"
              :label="{text: String(index+1), color: '#FFFFFF', fontSize: '20px'}"
              @click="center=m.position"
            />
          </GmapMap>
        </div>
      </div>
       <div v-if="isPostUser">
          <button @click="editPage">投稿を編集</button>
          <button @click="deletePost">投稿を削除</button>
        </div>
        <div v-else>
          <button @click="editPage">この投稿をコピーして旅程を作成</button>
        </div>
      <section class="comment-container">
        <h4>この記事に対するコメント</h4>
        <div class="comment-list-wrapper" ref="comment_list_wrapper">
          <ul class="comment-list" ref="comment_list">
            <li
              v-for="(comment_information, index) in comment_informations"
              :key="index"
              class="comment"
            >
              <b-icon icon="person-fill" class="user-icon" />
              <div class="sentence">
                <p>{{ comment_information.comment }}</p>
              </div>
            </li>
          </ul>
        </div>
        <div v-if="isLogin" class="send-comment">
          <h4>コメントを送る</h4>
          <div class="input-comment">
            <textarea v-model="new_comment" placeholder="コメントを入力" />
            <b-button @click="sendComment" variant="primary" class="send-button">送信</b-button>
          </div>
        </div>
        <div v-else class="request-login">
          <p class="m-0">※コメントをするにはログインが必要です。</p>
          <b-button variant="primary" @click="toLogin">ログイン</b-button>
        </div>
      </section>
    </div>
    <FloatingButton />
  </div>
</template>

<script>
/* eslint-disable */
import FloatingButton from '../components/FloatingButton';
import { gmapApi } from 'vue2-google-maps';

export default {
  components: {
    FloatingButton,
  },
  data() {
    return {
      isLogin: this.$store.getters.getUserName === '' ? false : true,
      post_id: -1,
      results: {
        post_information: {},
        schedule_information: [],
      },
      isPostUser: false,
      comment_informations: [],
      new_comment: '',
    };
  },
  computed: {
    google: gmapApi,
  },
  // sakuta↓
  async created() {
    const self = this;

    const path = process.env.VUE_APP_BASE_URL + 'api/getpost';
    const post_id = this.$router
      .resolve({ name: 'Detail' })
      .href.replace('/detail/', '');
    this.post_id = post_id;

    await this.$api
      .get(path, { params: { post_id: post_id } })
      .then(response => {
        self.results = response.data;
      })
      .catch(error => {
        console.log(error);
      });
    if (this.results.post_information.user_name === this.$store.state.userName) {
      this.isPostUser = true
    }
    await this.getComments();
  }, // sakuta↑
  mounted() {
    this.$refs.mapRef.$mapPromise.then(map => {
      map.fitBounds(this.getBound(), 10);
    });
  },

  methods: {
    getCenter() {
      if (this.results.schedule_information.length === 0) {
        return { lat: 35.681236, lng: 139.767125 };
      } else {
        var latSum = 0;
        var lngSum = 0;
        var count = 0;
        for (var i = 0; i < this.results.schedule_information.length; i++) {
          latSum = latSum + this.results.schedule_information[i].latitude;
          lngSum = lngSum + this.results.schedule_information[i].longitude;
          count += 1;
        }
        var locationCenterObj = {
          lat: latSum / count,
          lng: lngSum / count,
        };
        return locationCenterObj;
      }
    },
    getBound() {
      var maxlat = 0; //最大緯度
      var maxlng = 0; //最大経度
      var minlat = 0; //最小緯度
      var minlng = 0; //最小経度

      if (this.results.schedule_information.length === 0) {
        maxlat = 45;
        maxlng = 140;
        minlat = 35;
        minlng = 135;
      } else {
        for (var i = 0; i < this.results.schedule_information.length; i++) {
          if (i === 0) {
            maxlat = this.results.schedule_information[i].latitude;
            minlat = this.results.schedule_information[i].latitude;
            maxlng = this.results.schedule_information[i].longitude;
            minlng = this.results.schedule_information[i].longitude;
          }
          if (this.results.schedule_information[i].latitude > maxlat) {
            maxlat = this.results.schedule_information[i].latitude;
          } else if (this.results.schedule_information[i].latitude < minlat) {
            minlat = this.results.schedule_information[i].latitude;
          }
          if (this.results.schedule_information[i].longitude > maxlng) {
            maxlng = this.results.schedule_information[i].longitude;
          } else if (this.results.schedule_information[i].longitude < minlng) {
            minlng = this.results.schedule_information[i].longitude;
          }
        }
      }
      //北西端の座標を設定
      var sw = new this.google.maps.LatLng(maxlat, minlng);
      //東南端の座標を設定
      var ne = new this.google.maps.LatLng(minlat, maxlng);
      //範囲を設定
      var bounds = new this.google.maps.LatLngBounds(sw, ne);
      //自動調整
      return bounds;
    },
    editPage() {
        const postID = this.$router
        .resolve({ name: 'Detail' })
        .href.replace('/detail/', '');
        this.$router.push({ name: "Post", params: { post_id : postID, info: this.results}}).catch(() => {});
    },
    async getComments() {
      const self = this;
      const path =
        process.env.VUE_APP_BASE_URL +
        'api/getcomments?post_id=' +
        this.post_id;
      await this.$api
        .get(path)
        .then(response => {
          const comments = response.data;
          if (comments.length > 0) {
            comments.sort((a, b) => {
              return a.comment_time > b.comment_time ? 1 : -1;
            });
            self.comment_informations = comments;
          }
        })
        .catch(error => console.log(error));
      self.scrollToBottom();
    },
    sendComment() {
      const new_comment = this.new_comment;
      if (new_comment === '') return;

      const self = this;
      const path = process.env.VUE_APP_BASE_URL + 'api/addcomment';

      let params = new URLSearchParams();
      const user_name = this.$store.getters.getUserName;
      params.append('commenter_name', user_name);
      params.append('post_id', self.post_id);
      params.append('comment', new_comment);
      console.log(params.values().next());
      this.$api
        .post(path, params)
        .then(async response => {
          console.log(response);
          self.new_comment = '';
          self.getComments();
        })
        .catch(error => console.log(error));
    },
    scrollToBottom() {
      const comment_list_wrapper = this.$refs.comment_list_wrapper;
      const comment_list = this.$refs.comment_list;
      comment_list_wrapper.scrollTop = comment_list.clientHeight + 20;
    },
    toLogin() {
      this.$router.push({ path: '/login' });
    },
    deletePost() {
      const self = this;
      const path = process.env.VUE_APP_BASE_URL + 'api/postdelete';

      let params = new URLSearchParams();
      const user_name = this.$store.getters.getUserName;
      params.append('post_id', self.post_id);
      params.append('user_name', user_name);
      console.log(params.values().next());
      this.$api
        .post(path, params)
        .then(async response => {
          console.log(response);
        })
        .catch(error => console.log(error));
      this.$router.push({ path: '/' });
    },
  },
};
</script>

<style lang="scss" scoped>
.detail {
  text-align: center;
  color: #2c3e50;
  margin: 0 auto;

  p {
    font-size: 20px;
  }

  .schedule {
    margin: 20px;

    .schedule-container {
      background-color: rgb(207, 225, 231);
      width: 1200px;
      display: flex;
      margin: auto;
      padding: 10px 50px;
      border-radius: 6px;

      .plan {
        padding: 10px;
        display: inline-block;
        text-align: left;

        .trip-title {
          margin: 0px 0px 30px 0px;

          h3 {
            text-align: left;
            margin: 50px 0 30px;
          }
        }

        .vue-tbl {
          border: 2px solid #368c97;
          border-radius: 3px;
          background-color: #fff;

          th {
            background-color: #368c97;
            color: rgba(255, 255, 255, 0.66);
          }

          td {
            background-color: #f9f9f9;
          }

          th,
          td {
            min-width: 120px;
            padding: 5px;
          }
        }
      }

      #gmap {
        margin: 40px 20px;
      }
    }

    .comment-container {
      width: 1200px;
      margin: 50px auto;
      text-align: left;

      h4 {
        font-weight: bold;
      }

      .comment-list-wrapper {
        min-height: 100px;
        max-height: 500px;
        overflow: scroll;
        border: #ccc 1px solid;

        .comment-list {
          list-style: none;
          margin-bottom: 0;
          padding: 0 20px;

          .comment {
            display: flex;
            align-items: center;
            padding: 20px 0;

            .user-icon {
              font-size: 42px;
              margin-right: 10px;
            }

            .sentence {
              position: relative;
              display: inline-block;
              max-width: 90%;
              border-radius: 0.3em;
              background-color: rgb(207, 225, 231);

              &::before {
                content: '';
                position: absolute;
                top: 50%;
                left: -30px;
                margin-top: -15px;
                border: 15px solid transparent;
                border-right: 15px solid rgb(207, 225, 231);
              }

              p {
                max-width: 100%;
                margin: 0;
                padding: 10px;
                word-wrap: break-word;
              }
            }
          }
        }
      }

      .send-comment {
        margin-top: 50px;

        .input-comment {
          position: relative;

          textarea {
            width: 100%;
            height: 100px;
          }

          .send-button {
            position: absolute;
            right: 5px;
            bottom: 10px;
          }
        }
      }

      .request-login {
        display: flex;
        align-items: center;
        margin-top: 10px;

        p {
          font-size: 16px;
        }
      }
    }
  }
}

button {
  border: none;
  cursor: pointer;
  outline: none;
  margin: 10px ;
  //   padding: 8px 16px;
  padding: 8px 10px;
  appearance: none;
  border-radius: 6px;
}

img {
  width: 100%;
  height: 260px;
  object-fit: contain;
  margin: 10px;
}

</style>
