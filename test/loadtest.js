import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 2000 },
    { duration: '1m', target:  3500 },
    { duration: '30s', target: 2800 },
    { duration: '30s', target: 1500 },
  ],
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<500'],
  },
};


export default function () {
  const localStore = {
    predictedId: null,
  };

  const randomValue = Math.floor(Math.random() * 1000);
  const postUrl = `http://localhost:8000/api/predicts/${randomValue}`;
  const postResponse = http.post(postUrl);
  
  check(postResponse, {
    'POST status is 200': (r) => r.status === 200,
    'POST returns prediction ID': (r) => {
      if (r.status === 200) {
        localStore.predictedId = r.json('prediction_id'); // Сохраняем ID локально для этого VU
        return true;
      }
      return false;
    },
  });

  if (localStore.predictedId) {
    const getUrl = `http://localhost:8000/api/predicts/${localStore.predictedId}`;
    const getResponse = http.get(getUrl);
    
    check(getResponse, {
      'GET status is 200': (r) => r.status === 200
    });
  }

  sleep(1);
}