import { createApp } from "vue";
import App from "./App.vue";
import { initializeApp } from "firebase/app";

const firebaseConfig = {
  apiKey: "AIzaSyD0xinG-cLHv0jPKDYNSufwi-lbN1GnBE0",
  authDomain: "gramatiquizz.firebaseapp.com",
  projectId: "gramatiquizz",
  storageBucket: "gramatiquizz.firebasestorage.app",
  messagingSenderId: "907838437779",
  appId: "1:907838437779:web:be41c319bdedcfd67d5066",
};

const firebaseApp = initializeApp(firebaseConfig);

const app = createApp(App);
app.use({
  install(app) {
    app.provide("firebase", firebaseApp);
  },
});
app.mount("#app");
