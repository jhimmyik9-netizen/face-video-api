Feature: Face Video Analysis API

  Background:
    * url baseUrl

  Scenario: Health endpoint reports service status
    Given path 'health'
    When method get
    Then status 200
    And match response.status == 'ok'

  Scenario: Unsupported upload format is rejected
    Given path 'analyze'
    And multipart file file = { read: 'classpath:fixtures/notes.txt', filename: 'notes.txt', contentType: 'text/plain' }
    When method post
    Then status 415
    And match response.detail contains 'Formato no admitido'
