/** @type {import('@playwright/test').PlaywrightTestConfig} */
const config = {
  timeout: 30 * 1000,
  use: {
    headless: true,
    viewport: { width: 1280, height: 800 },
    ignoreHTTPSErrors: true,
    baseURL: process.env.BASE_URL || 'http://127.0.0.1:5000'
  },
  testDir: './tests'
};

module.exports = config;
