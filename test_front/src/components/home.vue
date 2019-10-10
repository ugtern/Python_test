<template>
  <div>
    <div>
      <input type="text" v-model="login">
      <input type="password" v-model="password">
      <br>
      <br>
      <button @click="reg" class="main_click">Регистрация</button>
    </div>
      <br>
      <br>
    <div>
      <input type="text" v-model="login">
      <input type="password" v-model="password">
      <br>
      <br>
      <button @click="authoriz" class="main_click">Авторизация</button>
    </div>
  </div>
</template>

<script>
    export default {
        name: "home",
        data() {
            return {
                login: '',
                password: '',
                one: 23,
                two: 27,
            }
        },
        methods: {
            authoriz() {
                $.ajax({
                    url: 'http://0.0.0.0:8088/auth/',
                    type: 'POST',
                    data: JSON.stringify({
                        login: this.login,
                        password: this.password,
                    }),
                    dataType: 'json',
                    success: (response) => {
                        sessionStorage.setItem('auth_token', response.token);
                    },
                    error: (response) => {
                        alert('Ошибка')
                    }
                })
            },
            reg() {
                $.ajax({
                    url: 'http://0.0.0.0:8088/reg/',
                    type: 'POST',
                    data: JSON.stringify({
                        login: this.login,
                        password: this.password,
                    }),
                    dataType: 'json',
                    success: (responce) => {
                        console.log('complete')
                    },
                    error: (responce) => {
                        console.log('error')
                    },
                })
            }
        }
    }
</script>

<style scoped>
  .main_click {
    height: 40px;
    width: 200px;
    background-color: #2c3e50;
    color: white;
  }
</style>
