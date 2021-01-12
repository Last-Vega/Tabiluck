<!-- nakano -->
<template>
  <div class="post">
      <div v-if="this.info != null && this.info.post_information.user_name === this.$store.state.userName">
          <h1>投稿の編集</h1>
      </div>
    <div v-else>
       <h1>新規投稿</h1>
    </div>
    <div class="schedule-container">
      <div class="plan">
        <div class="trip_title">
          <h4>旅行タイトル</h4>
          <input v-model="postName" placeholder="例：2泊3日長崎旅行" />
        </div>
        <div class="trip_title">
          <h4>本文</h4>
          <textarea v-model="content" placeholder="例：楽しかったです！"></textarea>
          <Upload v-model="picture" />
          <!-- <img :src="picture.image" /> -->
        </div>
        <table class="vue_tbl">
          <thead>
            <tr>
              <th>Dates</th>
              <th>Location</th>
              <th>Transportation</th>
              <th>Memo</th>
              <th>Edit</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(schedule, i) in schedules" :key="i">
              <td>{{ schedule.year }}年{{ schedule.month }}月{{ schedule.day }}日 {{ schedule.startHour }}:{{ schedule.startMin }}〜{{ schedule.endHour }}:{{ schedule.endMin }}</td>
              <td>{{ schedule.locationName }}</td>
              <td>{{ schedule.transportation }}</td>
              <td>{{ schedule.memo }}</td>
              <td>
                <div id="modal">
                  <button v-on:click="setInitialValue(i)">編集</button>
                  <button v-on:click="deleteSchedule(i)">削除</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
        <div id="modal">
          <button v-on:click="openModal">スケジュールを追加</button>
          <Modal v-show="showContent" v-on:from-child="closeModal">
            <template slot="send">
              <!-- <p>場所：<input v-model="locationName"></p> -->
              <p>
                場所：
                <input v-model="locationName" />
                <button @click="findLatLng">位置情報を登録</button>
              </p>
              <div id="modal-gmap">
                <GmapMap
                  :center="location"
                  :zoom="15"
                  :options="{streetViewControl: false}"
                  map-type-id="terrain"
                  style="width: 450px; height: 230px"
                >
                  <GmapMarker
                    v-if="locationFlag"
                    :key="index"
                    :position="location"
                    :clickable="true"
                    :draggable="true"
                    @click="center=m.position"
                  />
                </GmapMap>
              </div>
              <p>
                日付：
                <Datepicker :format="dateFormat" v-model="dates" @closed="datePickerClosed"></Datepicker>
              </p>
              <p>
                開始時間：
                <vue-timepicker
                  :format="timeFormat"
                  :minute-interval="minInterval"
                  placeholder="時間"
                  hour-label="時"
                  minute-label="分"
                  v-model="startTime"
                />
              </p>
              <p>
                終了時間：
                <vue-timepicker
                  :format="timeFormat"
                  :minute-interval="minInterval"
                  placeholder="時間"
                  hour-label="時"
                  minute-label="分"
                  v-model="endTime"
                />
              </p>
              <p>
                交通手段：
                <select v-model="transportation">
                  <option>車</option>
                  <option>電車</option>
                  <option>バス</option>
                  <option>飛行機</option>
                  <option>船</option>
                  <option>徒歩</option>
                  <option>その他</option>
                </select>
              </p>
              <p>
                メモ：
                <textarea v-model="memo" placeholder="add memo"></textarea>
              </p>
              <button @click="doSend">スケジュールを登録</button>
            </template>
          </Modal>
        </div>
      </div>
      <div id="gmap">
        <GmapMap
          ref="mapRef"
          :center="getCenter()"
          :zoom="9"
          :options="{streetViewControl: false,}"
          map-type-id="terrain"
          style="width: 400px; height: 300px"
        >
          <GmapMarker
            :key="index"
            v-for="(schedule, index) in schedules"
            :position="schedule.location"
            :clickable="true"
            :draggable="true"
            :icon="{fillColor: '#ff8c00', fillOpacity: 0.8, path: google.maps.SymbolPath.CIRCLE, scale: 16, strokeColor: '#ff8c00',strokeWeight: 1.0}"
            :label="{text: String(index+1), color: '#FFFFFF', fontSize: '20px'}"
            @click="center=m.position"
          />
        </GmapMap>
      </div>
    </div>
    <button class="post-button" @click="postConfirm()">投稿する</button>
  </div>
</template>

<script>
// @ is an alias to /src
/* eslint-disable */
import Modal from '@/components/Modal.vue';
import Upload from '@/components/Upload.vue';
import Vue from 'vue';
import { gmapApi } from 'vue2-google-maps';
import Datepicker from 'vuejs-datepicker';
import VueTimepicker from 'vue2-timepicker';
import 'vue2-timepicker/dist/VueTimepicker.css';
import moment from 'moment';

export default {
  name: 'Post',
  components: {
    Modal,
    Upload,
    Datepicker,
    'vue-timepicker': VueTimepicker,
  },
  props: {
    post_id: String,
    info: Object,
  },
  data() {
    return {
      showContent: false,
      locationName: '',
      location: { lat: 35.681236, lng: 139.767125 },
      year: '2020',
      month: '08',
      day: '01',
      startHour: '12',
      startMin: '00',
      endHour: '13',
      endMin: '00',
      transportation: '',
      memo: '',
      schedules: [],
      index: '',
      count: '0',
      markers: [],
      locationFlag: false,
      postName: '',
      content: '',
      picture: { image: null, imageName: null },
      dates: '2020-08-01',
      dateFormat: 'yyyy-MM-dd',
      timeFormat: 'HH:mm', // 形式 AMなどの指定もできる
      minInterval: 5, // 分の間隔 これは5分ごとの設定
      startTime: '12:00',
      endTime: '13:00',
    };
  },
  mounted() {
    if (this.info != null) {
      var postInfo = this.info.post_information;
      var scheduleInfo = this.info.schedule_information;
      this.postName = postInfo.post_name;
      this.content = postInfo.content;
      this.picture = {
        image: postInfo.image_base64,
        imageName: postInfo.image_name,
      };
      for (var i = 0; i < scheduleInfo.length; i++) {
        var s = scheduleInfo[i];
        this.schedules.push({});
        this.$set(this.schedules[i], 'locationName', s.title);
        this.$set(this.schedules[i], 'location', {
          lat: s.latitude,
          lng: s.longitude,
        });
        this.$set(this.schedules[i], 'year', s.start_year);
        this.$set(this.schedules[i], 'month', ('0' + s.start_month).slice(-2));
        this.$set(this.schedules[i], 'day', ('0' + s.start_date).slice(-2));
        this.$set(this.schedules[i], 'startHour', ('00' + s.start_hour).slice(-2));
        this.$set(this.schedules[i], 'startMin', ('00' + s.start_min).slice(-2));
        this.$set(this.schedules[i], 'endHour', ('00' + s.end_hour).slice(-2));
        this.$set(this.schedules[i], 'endMin', ('00' + s.end_min).slice(-2));
        this.$set(this.schedules[i], 'transportation', s.transportation);
        this.count++;
      }
      this.$refs.mapRef.$mapPromise.then(map => {
        map.fitBounds(this.getBound(), 10);
      });
    }
  },
  methods: {
    openModal() {
      this.showContent = true;
    },
    closeModal() {
      this.showContent = false;
    },
    doSend() {
      this.startHour = this.startTime.slice(0, 2);
      this.startMin = this.startTime.slice(3, 5);
      this.endHour = this.endTime.slice(0, 2);
      this.endMin = this.endTime.slice(3, 5);
      if (this.locationName.length === 0) {
        alert('場所を入力してください');
      } else if (
        this.month.length === 0 ||
        this.year.length === 0 ||
        this.day.length === 0
      ) {
        alert('日付を選択してください');
      } else if (
        this.startHour.length === 0 ||
        this.startMin.length === 0 ||
        this.endHour.length === 0 ||
        this.endMin.length === 0
      ) {
        alert('時間を選択してください');
      } else if (this.transportation === '') {
        alert('ここまでの交通手段を選択してください');
      } else {
        // index.lengthがnullでないとき，
        // 新規作成(schedulesに新たにobjectを追加)
        // それ以外はthis.index使って上書き
        if (!(this.index.length == null)) {
          this.schedules.push({});
          this.index = this.count;
          this.count++;
        }
        if (!this.locationFlag) {
          this.location = { lat: '', lng: '' };
          this.locationFlag = true;
        }
        // alert(this.locationName + this.month + this.day + this.startTime + this.endTime + this.transportation + this.memo)
        this.$set(
          this.schedules[this.index],
          'locationName',
          this.locationName
        );
        this.$set(this.schedules[this.index], 'location', this.location);
        this.$set(this.schedules[this.index], 'year', this.year);
        this.$set(this.schedules[this.index], 'month', this.month);
        this.$set(this.schedules[this.index], 'day', this.day);
        this.$set(this.schedules[this.index], 'startHour', this.startHour);
        this.$set(this.schedules[this.index], 'startMin', this.startMin);
        this.$set(this.schedules[this.index], 'endHour', this.endHour);
        this.$set(this.schedules[this.index], 'endMin', this.endMin);
        this.$set(
          this.schedules[this.index],
          'transportation',
          this.transportation
        );
        this.$set(this.schedules[this.index], 'memo', this.memo);
        this.locationName = '';
        this.location = { lat: 35.681236, lng: 139.767125 };
        this.year = '2020';
        this.month = '08';
        this.day = '01';
        this.startHour = '12';
        this.startMin = '00';
        this.endHour = '13';
        this.endMin = '00';
        this.transportation = '';
        this.memo = '';
        this.index = '';
        this.locationFlag = false;
        this.dates = '2020-08-01';
        this.startTime = '12:00';
        this.entTime = '13:00';
        this.schedules.sort(function(a, b) {
          if (a.year > b.year) return 1;
          if (a.year < b.year) return -1;
          if (Number(a.month) > Number(b.month)) return 1;
          if (Number(a.month) < Number(b.month)) return -1;
          if (Number(a.day) > Number(b.day)) return 1;
          if (Number(a.day) < Number(b.day)) return -1;
          if (Number(a.startHour) > Number(b.startHour)) return 1;
          if (Number(a.startHour) < Number(b.startHour)) return -1;
          if (Number(a.startMin) > Number(b.startMin)) return 1;
          if (Number(a.startMin) < Number(b.startMin)) return -1;
          return 0;
        });
        this.closeModal();
      }
    },
    setInitialValue(index) {
      this.index = index;
      this.locationName = this.schedules[index].locationName;
      this.location = this.schedules[index].location;
      this.year = this.schedules[index].year;
      this.month = this.schedules[index].month;
      this.day = this.schedules[index].day;
      this.startHour = this.schedules[index].startHour;
      this.startMin = this.schedules[index].startMin;
      this.endHour = this.schedules[index].endHour;
      this.endMin = this.schedules[index].endMin;
      this.transportation = this.schedules[index].transportation;
      this.memo = this.schedules[index].memo;
      this.dates = this.year + '-' + this.month + '-' + this.day;
      this.startTime = this.startHour + ':' + this.startMin;
      this.endTime = this.endHour + ':' + this.endMin;
      this.locationFlag = true;
      this.openModal();
    },
    deleteSchedule(index) {
      this.schedules.splice(index, 1);
      this.count--;
    },
    findLatLng() {
      Vue.$geocoder.setDefaultMode('address');
      var addressObj = {
        address_line_1: this.locationName,
      };
      Vue.$geocoder.send(addressObj, response => {
        if (response.status === 'OK') {
          this.location = response.results[0].geometry.location;
          this.locationFlag = true;
        }
      });
    },
    getCenter() {
      if (this.schedules.length === 0) {
        return { lat: 35.681236, lng: 139.767125 };
      } else {
        var latSum = 0;
        var lngSum = 0;
        var count = 0;
        for (var i = 0; i < this.schedules.length; i++) {
          if (this.schedules[i].location.lat.length == 0) continue;
          latSum = latSum + this.schedules[i].location.lat;
          lngSum = lngSum + this.schedules[i].location.lng;
          count += 1;
        }
        var locationCenterObj = {
          lat: latSum / count,
          lng: lngSum / count,
        };
        this.mapReload();
        return locationCenterObj;
      }
    },
    getBound() {
      var maxlat = 0; //最大緯度
      var maxlng = 0; //最大経度
      var minlat = 0; //最小緯度
      var minlng = 0; //最小経度

      if (this.schedules.length === 0) {
        maxlat = 45;
        maxlng = 140;
        minlat = 35;
        minlng = 135;
      } else {
        for (var i = 0; i < this.schedules.length; i++) {
          if (this.schedules[i].location.lat.length == 0) continue;
          if (i === 0) {
            maxlat = this.schedules[i].location.lat;
            minlat = this.schedules[i].location.lat;
            maxlng = this.schedules[i].location.lng;
            minlng = this.schedules[i].location.lng;
          }
          if (this.schedules[i].location.lat > maxlat) {
            maxlat = this.schedules[i].location.lat;
          } else if (this.schedules[i].location.lat < minlat) {
            minlat = this.schedules[i].location.lat;
          }
          if (this.schedules[i].location.lng > maxlng) {
            maxlng = this.schedules[i].location.lng;
          } else if (this.schedules[i].location.lng < minlng) {
            minlng = this.schedules[i].location.lng;
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
    mapReload() {
      this.$refs.mapRef.$mapPromise.then(map => {
        map.fitBounds(this.getBound(), 10);
      });
    },
    postConfirm() {
      if (this.postName.length === 0) {
        alert('旅のタイトルを入力してください');
      } else if (this.content.length === 0) {
        alert('本文を選択してください');
      } else if (this.schedules.length === 0) {
        alert('スケジュールを登録してください');
      } else {
        this.post();
        this.$router.push({ path: '/' });
      }
    },
    post() {
      // const self = this
      var path = process.env.VUE_APP_BASE_URL + 'api/postschedule';
      var params = {
        post_information: {
          user_name: this.$store.state.userName,
          post_name: this.postName,
          content: this.content,
        },
        schedule_information: [],
      };
      if (this.picture.image != null) {
        params.post_information.image = this.picture.image;
        params.post_information.image_name = this.picture.imageName;
      }
      if (this.info != null) {
        if (this.info.post_information.user_name === this.$store.state.userName) {
          path = process.env.VUE_APP_BASE_URL + 'api/postedit';
          params.post_information.post_id = this.post_id
        }
      }
      for (var i = 0; i < this.schedules.length; i++) {
        var s = this.schedules[i];
        params.schedule_information.push({
          title: s.locationName,
          latitude: s.location.lat,
          longitude: s.location.lng,
          start_year: s.year,
          start_month: s.month,
          start_date: s.day,
          start_hour: s.startHour,
          start_min: s.startMin,
          end_year: s.year,
          end_month: s.month,
          end_date: s.day,
          end_hour: s.endHour,
          end_min: s.endMin,
          transportation: s.transportation,
          memo: s.memo,
        });
      }
      console.log(params);
      this.$api
        .post(path, params)
        .then(res => console.log(res.data))
        .catch(e => console.log(e));
    },
    datePickerClosed() {
      if (this.dates) {
        this.dates = moment(this.dates).format('YYYY-MM-DD');
        this.year = this.dates.slice(0, 4);
        this.month = this.dates.slice(5, 7);
        this.day = this.dates.slice(8, 10);
      }
    },
    getPath() {
      var path = [];
      for (var i = 0; i < this.schedules.length; i++) {
        if (this.schedules[i].location.lat.length == 0) continue;
        path.push(this.schedules[i].location);
      }
      return path;
    },
  },
  computed: {
    google: gmapApi,
  },
  created() {
    if (this.$store.state.userName === '') {
      this.$router.push({ path: '/' });
    }
  },
};
</script>


<style scoped lang="scss">
.post {
  margin: 20px;
}

.schedule-container {
  background-color: rgb(207, 225, 231);
  width: 1200px;
  display: flex;
  margin: auto;
  padding: 10px 50px;
  border-radius: 6px;
}

.plan {
  // background-color: lightblue;
  padding: 10px;
  display: inline-block;
  text-align: left;
}

.trip_title {
  margin: 0px 0px 30px 0px;
}

button {
  border: none;
  cursor: pointer;
  outline: none;
  margin: 20px auto;
  //   padding: 8px 16px;
  padding: 8px 10px;
  appearance: none;
  border-radius: 6px;
}

#modal {
  text-align: left;
}

table {
  border: 2px solid #368c97;
  border-radius: 3px;
  background-color: #fff;
}

th {
  background-color: #368c97;
  color: rgba(255, 255, 255, 0.66);
  cursor: pointer;
}

td {
  background-color: #f9f9f9;
}

th,
td {
  min-width: 120px;
  padding: 5px;
}

#modal-gmap {
  margin: 0px 0px 10px 0px;
}

#gmap {
  margin: 110px 20px;
}
</style>
