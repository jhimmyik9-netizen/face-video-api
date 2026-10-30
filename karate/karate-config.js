function fn() {
  var config = {};
  config.baseUrl = karate.properties['baseUrl'] || 'http://127.0.0.1:8000';
  return config;
}
