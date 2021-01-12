<!-- sakuta -->
<template>
  <div class="buttons">
    <button class="traveled" :class="leftButtonColor()" @click="leftButtonPush">旅行済み</button>
    <button class="traveling" :class="rightButtonColor()" @click="rightButtonPush">旅行予定</button>
  </div>
</template>

<script>
/* eslint-disable */
export default {
  data() {
    return {
      isActive: 1,
    };
  },
  methods: {
    leftButtonColor() {
      if (this.isActive == 1) {
        return {
          orange: true,
        };
      } else {
        return {
          blue: true,
        };
      }
    },
    rightButtonColor() {
      if (this.isActive == 0) {
        return {
          orange: true,
        };
      } else {
        return {
          blue: true,
        };
      }
    },
    leftButtonPush() {
      this.isActive = 1;
      this.$emit('buttonActive', this.isActive);
    },
    rightButtonPush() {
      this.isActive = 0;
      this.$emit('buttonActive', this.isActive);
    },
  },
};
</script>

<style lang="scss" scoped>
button {
  border: none;
  cursor: pointer;
  outline: none;
  padding: 8px 16px;
  appearance: none;
  border-radius: 6px;
}
.orange {
  background-color: rgb(255, 155, 40);
  border-bottom: solid 4px darken(rgb(255, 155, 40), 20%);
  box-shadow: 0px 3px 3px rgba(0, 0, 0, 0.29);
  &:active {
    -webkit-transform: translateY(4px);
    transform: translateY(4px);
    border-bottom: none;
    box-shadow: 0px 0px 1px rgba(0, 0, 0, 0.2);
  }
}
.blue {
  background-color: rgb(83, 109, 255);
  border-bottom: solid 4px darken(rgb(83, 109, 255), 30%);
  box-shadow: 0px 3px 3px rgba(0, 0, 0, 0.29);
  &:active {
    -webkit-transform: translateY(4px);
    transform: translateY(4px);
    border-bottom: none;
    box-shadow: 0px 0px 1px rgba(0, 0, 0, 0.2);
  }
}
.traveled {
  margin-right: 40px;
}
</style>
