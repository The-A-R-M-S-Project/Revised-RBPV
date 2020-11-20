import Vue from 'vue';
// eslint-disable-next-line import/no-extraneous-dependencies
import Router from 'vue-router';
import Ping from './components/Ping.vue';
import Amortize from './components/Amortize.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/amortize',
      name: 'Amortize',
      component: Amortize,
    },
    {
      path: '/ping',
      name: 'Ping',
      component: Ping,
    },
  ],
});
