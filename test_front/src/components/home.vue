<template>
  <div>
    <div v-if="auth">
      <div class="test-interface-check-predict-ui">
        <h3>Выберите правильный класс</h3>
        <h5 v-model="current_message">{{current_message}}</h5>
        <select class="test-interface-send-ui test-interface-select_correct_class" v-model="selected_class">
          <option value="" hidden disabled selected>Выбрать ...</option>
          <option v-for="value in classes">{{value}}</option>
        </select>
        <button class="test-interface-sender test-interface-ui-elements" @click="send_correct_class">отправить</button>
      </div>
    </div>
    <div v-if="auth===false">
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
                auth: false,
                login: '',
                password: '',
                one: 23,
                two: 27,
                classes: [],
                selected_class: '',
                current_message: '',
                current_id: 0,
            }
        },
        created() {

            this.auth_method();

            $.ajax({
                url: 'http://0.0.0.0:8088/get_classes/',
                type: 'GET',
                dataType: 'json',
                success: (response) => {
                  this.classes = response.classes;
                },
                error: (response) => {
                    this.res_stat = 'Произошла ошибка пожалуйста обратитесь к разработчикам';
                    this.current_state = 'error';
                }
            })
        },
        methods: {
            auth_method() {
                if (sessionStorage.getItem('auth_token')) {
                    this.auth = true
                }
                else {
                    this.auth = false
                }
            },
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
                        sessionStorage.setItem('login', this.login)
                        sessionStorage.setItem('auth_token', response.token);
                        this.auth = true
                        this.get_next_message()
                    },
                    error: (response) => {
                        alert('Ошибка')
                    }
                })
            },
            get_next_message() {
                $.ajax({
                    url: 'http://0.0.0.0:8088/get_next_message/',
                    type: 'POST',
                    data: JSON.stringify({
                        login: sessionStorage.getItem('login'),
                        current_id: this.current_id,
                    }),
                    dataType: 'json',
                    success: (response) => {
                      this.current_message = response.current_message
                      this.current_id = response.current_id
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
            },
            send_correct_class() {
                $.ajax({
                    url: 'http://0.0.0.0:8088/set_correct_class/',
                    type: 'POST',
                    data: JSON.stringify({
                        login: sessionStorage.getItem('login'),
                        current_id: this.current_id,
                        correct_class: this.selected_class,
                    }),
                    dataType: 'json',
                    success: (response) => {
                      this.current_id = response.current_id
                      this.get_next_message()
                    },
                    error: (response) => {
                        alert('Ошибка')
                    }
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
