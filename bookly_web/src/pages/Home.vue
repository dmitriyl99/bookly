<template>
  <header class="p-3 mb-3 border-bottom">
    <div class="container">
      <div class="d-flex flex-wrap align-items-center justify-content-between">
        <a
          href="/"
          class="
            d-flex
            align-items-center
            mb-2 mb-lg-0
            text-dark text-decoration-none
          "
        >
          <img src="../assets/logo.png" width="84" />
          <span class="ms-5 fs-1">Букля</span>
        </a>
        <span class="text-muted">Команда Bookworm</span>
      </div>
    </div>
  </header>
  <div class="px-4 py-5 my-5 text-center">
    <img
      class="d-block mx-auto mb-4"
      src="../assets/logo.png"
      alt=""
      width="72"
    />
    <h1 class="display-5 fw-bold">Букля</h1>
    <div class="col-lg-6 mx-auto">
      <p class="lead mb-4">
        Рекомендательная система для читателей московских библиотек
      </p>
      <div class="mb-3">
        <label for="readerInput" class="form-label">Номер читателя</label>
        <input
          type="text"
          class="form-control"
          id="readerInput"
          v-model="readerInput"
          aria-describedby="emailHelp"
        />
        <div id="emailHelp" class="form-text mb-3">
          Введите номер читателя, чтобы получить его историю и рекомендации. Или
          оставьте поле пустым и получите топ-5 популярных книг
        </div>
        <button class="btn btn-primary" :disabled="loading" @click="onSubmit">
          Получить рекомендации
        </button>
      </div>
    </div>
  </div>
  <div class="container">
    <div v-if="history.length > 0">
      <h3>История</h3>
      <ul>
        <li v-for="book in history" :key="book.id">
          {{ book.title }} - {{ book.author }}
        </li>
      </ul>
    </div>
    <div v-if="recommendations.length > 0">
      <h3>Рекомендации</h3>
      <ul>
        <li v-for="book in recommendations" :key="book.id">
          {{ book.title }} - {{ book.author }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Home",
  data: function () {
    return {
      readerInput: null,
      loading: false,
      recommendations: [],
      history: [],
    };
  },
  methods: {
    onSubmit() {
      this.loading = true;
      let readerId = this.readerInput == null ? 0 : this.readerInput;
      axios
        .get(`http://localhost:8008/api/recommendation?reader_id=${readerId}`)
        .then((response) => {
          let data = response.data.data;
          this.recommendations = data.recommendations;
          this.history = data.history;
        })
        .finally(() => {
          this.loading = false;
        });
    },
  },
};
</script>