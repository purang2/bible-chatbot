// index.js
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";

// 모바일 Safari에서 viewport 높이 문제 해결
const setVhProperty = () => {
  const vh = window.innerHeight * 0.01;
  document.documentElement.style.setProperty("--vh", `${vh}px`);
};

window.addEventListener("resize", setVhProperty);
window.addEventListener("orientationchange", setVhProperty);
setVhProperty();

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
