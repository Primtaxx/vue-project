<!-- Games.vue -->
<template>
  <div>
    <div>
      <b-heading size="2" class="has-text-weight-bold has-text-centered is-size-1-desktop">Game Library</b-heading>
    </div>
    <add-game @add-game="addToLibrary"></add-game>
    <b-field>
      <b-button
          label="Clear selected"
          type="is-danger"
          icon-left="close"
          :disabled="!selected"
          @click="clearSelected" />
      <update-game v-if="selected" :selected-game="selected" @update-game="updateSelectedGame"></update-game>
    </b-field>

  <b-tabs>
    <b-tab-item label="Table">
        <b-table
            :data="games"
            :columns="columns"
            :selected="selected"
            @select="updateSelected"
            focusable>
        </b-table>
    </b-tab-item>

    <b-tab-item label="Selected">
        <pre>{{ selected }}</pre>
    </b-tab-item>
</b-tabs>
    <div>
      <p>Total Spent Time: {{ totalTimeSpent }} hours</p>
      <p>Total Price: ${{ totalPrice.toFixed(2) }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import AddGame from './AddGame.vue';
import UpdateGame from './UpdateGame.vue';


export default {
  components: {
    AddGame,
    UpdateGame,
  },
  data() {
    return {
      games: [],
      selected: null,
      columns: [
        {
          field: "appid",
          label: "ID",
          width: "40",
          numeric: true
        },
        {
          field: "name",
          label: "Name"
        },
        {
          field: "release_date",
          label: "Release Date"
        },
        {
          field: "developer",
          label: "Publisher"
        },
        {
          field: "price",
          label: "Price"
        },
        {
          field: "played",
          label: "Played?"
        },
        {
          field: "hours_played",
          label: "Hours Played"
        }
      ]
    };
  },


  mounted() {
    this.fetchGames();
  },
  methods: {
    async fetchGames() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/games');
        this.games = response.data;
      } catch (error) {
        console.error('Error fetching games:', error);
      }
    },
    async addToLibrary(game) {
      try {
        await axios.post('http://127.0.0.1:5000/games', game);
        this.games.push(game);
      } catch (error) {
        console.error('Error adding game:', error);
      }
    },
    async removeFromLibrary(appid) {
      try {
        await axios.delete(`http://127.0.0.1:5000/games/${appid}`);
        this.games = this.games.filter((g) => g.appid !== appid);
      } catch (error) {
        console.error('Error removing game:', error);
      }
    },
    async updateGame(appid) {
      const updates = {
        price: 9.99
      };
      try {
        await axios.put(`http://127.0.0.1:5000/games/${appid}`, updates);
        const game = this.games.find((g) => g.appid === appid);
        Object.assign(game, updates);
      } catch (error) {
        console.error('Error updating game:', error);
      }
    },
    clearSelectedGame() {
      if (this.selected) {
        this.removeFromLibrary(this.selected.appid);
        this.selected = null;
      }
    },
    updateSelected(newSelected) {
      this.selected = newSelected;
    },
    clearSelected() {
      if (this.selected) {
        this.removeFromLibrary(this.selected.appid);
        this.selected = null;
      }
    },
    async updateSelectedGame(updates) {
      if (this.selected) {
        try {
          await axios.put(`http://127.0.0.1:5000/games/${this.selected.appid}`, updates);
          const game = this.games.find((g) => g.appid === this.selected.appid);
          Object.assign(game, updates);
        } catch (error) {
          console.error('Error updating game:', error);
        }
      }
    },
  },
  computed: {
    totalTimeSpent() {
      return this.games.reduce((total, game) => total + parseFloat(game.hours_played || 0), 0);
    },
    totalPrice() {
      return this.games.reduce((total, game) => total + parseFloat(game.price || 0), 0);
    },
  },
};
</script>
