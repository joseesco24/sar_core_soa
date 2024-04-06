import { Httpx } from "https://jslib.k6.io/httpx/0.1.0/index.js";
import { check } from 'k6';

const session = new Httpx({
  baseURL: __ENV.K6_TARGET_HOST,
  timeout: 20000,
});

session.addHeader("Content-Type", "application/json");

export const options = {
  duration: "30s",
  vus: 30,
};

export default function testSuite() {
  const endpointPath = "/rest/user/search-by-email";
  const payload = JSON.stringify({
    email: "pedro.perez@correo.com.co",
  });

  const response = session.get(endpointPath, payload);

  check(response, {
    "is status 200": (response) => response.status === 200,
  });
}