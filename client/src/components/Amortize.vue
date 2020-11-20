<template>
  <div class="container-fluid">
    <h1>Good Morning!</h1>
    <h2>Welcome to CTF I</h2>
    <p id="pre-formatted">{{result}}</p>
    <p>{{trial}}</p>
<!--    <p id="pre-formated">{{res}}</p>-->
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Amortize',
  data() {
    return {
      msg: '',
    };
  },
  methods: {
    getMessage() {
      const path = 'http://localhost:5000/amortize';
      axios.get(path)
        .then((res) => {
          this.msg = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    this.getMessage();
  },
  computed: {
    result() {
      const { msg } = this;
      let result = '';
      for (let i = 0; i < msg.length; i += 1) {
        result += `${msg[i]}`;
      }
      return result;
    },
    trial() {
      const { msg } = this;
      let trial = '';
      for (let i = 2; i < msg.length; i += 3) {
        trial += `${msg[i]}`;
      }
      // const { msg } = this;
      // let trial = '';
      // let res = [];
      //
      // // try creating an array instead and put the lectures increased
      // // use v-for to display them in template
      //
      // for (let i = 0; i < msg.length; i += 1) {
      //   if (msg[i].includes('Day 0') === true) {
      //     for (let j = i + 1; j < 8; j += 1) {
      //       res += msg[j].substr(0, 9);
      //       trial += `${msg[j]}`;
      //     }
      //   }
      // }
      // return trial + res;
      return trial;
    },
  },
};
</script>

<style scoped>
  #pre-formatted {
  white-space: pre;
  color: #404040;
}
   #pre-formated {
  white-space: pre;
     color: #5bc0de;
}
#greet {
  color: #00A000;
  margin-left: 60px;
}
</style>
