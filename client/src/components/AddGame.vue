<template>
  <div>
    <b-button @click="toggleModal" type="is-primary">Add Game</b-button>
    <b-modal v-model="showModal" :can-cancel="['esc', 'outside']" @close="toggleModal">
      <div class="box">
        <div class="field">
          <label class="label">Filter by:</label>
          <div class="control">
            <div class="select">
              <select v-model="filterType">
                <option value="name">Title</option>
                <option value="publisher">Publisher</option>
                <option value="release_date">Release Date</option>
                <option value="price">Price</option>
              </select>
            </div>
          </div>
        </div>
        <div class="field">
          <label class="label">Search games</label>
          <div class="control">
            <input
              class="input"
              type="text"
              v-model="searchQuery"
              @input="searchGames"
              placeholder="Search games..."
            />
          </div>
        </div>
        <ul>
          <li v-for="game in searchResults" :key="game.appid">
            <b-button @click="addGame(game)">
              {{ game.name }} - {{ game.publisher }} - {{ game.release_date }} - ${{ game.price }}
            </b-button>
            <div>
              <input type="checkbox" v-model="game.played" />
              <label>Played</label>
            </div>
            <div v-if="game.played">
              <label>Hours played:</label>
              <input type="number" v-model="game.hours_played" />
            </div>
          </li>
        </ul>
      </div>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      searchQuery: '',
      searchResults: [],
      showModal: false,
      filterType: 'name',
    };
  },
  methods: {
    async searchGames() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/search_games', {
          searchQuery: this.searchQuery,
          filterType: this.filterType,
        });
        this.searchResults = response.data;
      } catch (error) {
        console.error('Error searching games:', error);
      }
    },
    addGame(game) {
      const gameToAdd = { ...game, played: game.played, hours_played: game.hours_played || 0 };
      this.$emit('add-game', gameToAdd);
      this.toggleModal();
    },
    toggleModal() {
      this.showModal = !this.showModal;
    },
  },
};
</script>
