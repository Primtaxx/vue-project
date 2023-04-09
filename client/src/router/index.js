import Vue from 'vue';
import Router from 'vue-router';
import Games from '../components/Games.vue';
import AddGames from '../components/AddGame.vue';
import Ping from '../components/Ping.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Games',
      component: Games,
    },
    {
      path: '/addgame',
      name: 'addGames',
      component: AddGames,
    },
    {
      path: '/ping',
      name: 'Ping',
      component: Ping,
    },

  ],
});
