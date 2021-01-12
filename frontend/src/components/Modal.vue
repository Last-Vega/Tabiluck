<!-- nakano -->
<template>
  <div id="overlay" v-on:click="clickEvent">
    <div id="content" v-on:click="stopEvent">
      <p>
        <slot name="send"></slot>
      </p>
    </div>
  </div>
</template>

<script>
/* eslint-disable */
export default {
  name: 'Modal',
  methods: {
    clickEvent: function() {
      this.$emit('from-child');
    },
    stopEvent: function() {
      event.stopPropagation();
    },
  },
};
</script>


<style scoped lang="scss">
#content {
  z-index: 10;
  width: 500px;
  padding: 1em;
  background:#fff;
  border-radius: 6px;
}

#overlay {
  /* 要素を重ねた時の順番 */

  z-index: 1;

  /* 画面全体を覆う設定 */
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);

  /* 画面の中央に要素を表示させる設定 */
  display: flex;
  align-items: center;
  justify-content: center;
}

button {
  border: none;
  cursor: pointer;
  outline: none;
  margin: 20px auto;
  padding: 8px 16px;
  appearance: none;
  border-radius: 6px;
}
</style>
