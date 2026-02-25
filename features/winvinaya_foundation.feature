Feature: WinVinaya Foundation Website
  As a user
  I want to verify the WinVinaya Foundation website
  So that I can ensure the page loads correctly with proper title and content

  Background:
    Given I navigate to WinVinaya Foundation website

  @smoke @winvinaya
  Scenario: Verify page title is present
    Then the page title should be present
    And I should be able to see the page title

  @smoke @winvinaya
  Scenario: Verify page title content
    Then the page title should contain "WinVinaya"

  @regression @winvinaya
  Scenario: Verify page main heading
    Then the main heading should contain "WinVinaya" or "Reflections"

  @regression @winvinaya
  Scenario: Verify logo presence
    Then the WinVinaya logo should be visible
  
  @regression @smoke @winvinaya
  Scenario: Verify navigation menu
    Then the navigation menu should be visible