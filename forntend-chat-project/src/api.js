import axios from 'axios';
import { ACCESS_TOKEN } from './token';


// const apiUrl = "/choreo-apis/awbo/backend/rest-api-be2/v1.0";


const api = axios.create({
//   baseURL: import.meta.env.VITE_API_URL ? import.meta.env.VITE_API_URL : apiUrl,
     baseURL: 'http://127.0.0.1:8001/chat/',
})


api.interceptors.request.use(
  (config) => {
    const accessToken = localStorage.getItem(ACCESS_TOKEN);
    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`;
    }
    return config;
  },
  (error) => {
    Promise.reject(error);
  }
  
);

export default api;