<!-- UpdateGame.vue -->
<template>
  <div>
    <b-field label="Played">
      <b-switch v-model="played"></b-switch>
    </b-field>
    <b-field label="Hours Played">
      <b-input v-model="hours_played" type="number" min="0"></b-input>
    </b-field>
    <b-button type="is-info" @click="update">Update selected game</b-button>
  </div>
</template>

<script>
export default {
  props: {
    selectedGame: Object
  },
  data() {
    return {
      played: this.selectedGame.played,
      hours_played: this.selectedGame.hours_played
    };
  },
  watch: {
    selectedGame(newVal) {
      this.played = newVal.played;
      this.hours_played = newVal.hours_played;
    }
  },
  methods: {
    update() {
      this.$emit('update-game', {
        appid: this.selectedGame.appid,
        played: this.played,
        hours_played: this.hours_played
      });
    }
  }
};
</script>
